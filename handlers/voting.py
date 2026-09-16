from telegram.error import TelegramError

from game import GameError, Phase
from handlers.common import current, group_command, require_manager, service
from handlers.lobby import add_player, remove_player
from keyboards import (
    accuse_keyboard,
    lobby_lang_keyboard,
    lobby_time_keyboard,
    menu_back_keyboard,
    menu_lang_keyboard,
    start_menu_keyboard,
    vote_keyboard,
)
from locations import format_location, get_locations
from texts import tr


async def begin_vote(svc, game, accuser, accused):
    lang = getattr(game, "lang", "uz")
    seconds = game.accuse(accuser, accused, svc.clock())
    svc.storage.save(game)
    svc.schedule(game, "vote", game.vote_deadline - svc.clock())
    sent = await svc.send(
        game.chat_id,
        tr(
            "voting",
            lang=lang,
            accuser=game.players[accuser].name,
            accused=game.players[accused].name,
            seconds=seconds,
            needed=len(game.players) // 2 + 1,
        ),
        reply_markup=vote_keyboard(game),
        parse_mode="Markdown",
    )
    if sent is None:
        await svc.cancel(game)


@group_command
async def accuse(update, context):
    svc = service(context)
    game = current(svc, update.effective_chat.id)
    game.require(Phase.ACTIVE, "active_only")
    uid = update.effective_user.id
    game.require_player(uid)
    target = None
    if context.args:
        username = context.args[0].lstrip("@").casefold()
        target = next(
            (
                p.id
                for p in game.players.values()
                if p.username and p.username.casefold() == username
            ),
            None,
        )
        if len(context.args) != 1 or target is None:
            raise GameError("target_missing")
    elif update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        if not user or user.id not in game.players:
            raise GameError("target_missing")
        target = user.id
    if target is None:
        lang = getattr(game, "lang", "uz")
        await update.message.reply_text(
            tr("select_accused", lang=lang),
            reply_markup=accuse_keyboard(game, uid),
        )
        return
    await begin_vote(svc, game, uid, target)


async def callback(update, context):
    query = update.callback_query
    try:
        await query.answer()
    except TelegramError:
        pass
    svc = service(context)
    try:
        parts = (query.data or "").split(":")
        action = parts[0]

        # Private chat navigation menu callbacks
        if action == "m":
            if update.effective_chat.type != "private":
                return
            bot_username = getattr(context.bot, "username", None) or "SpyfallBot"
            user_id = update.effective_user.id
            user_lang = "uz"
            if hasattr(svc.storage, "get_user_lang"):
                user_lang = svc.storage.get_user_lang(user_id) or "uz"

            sub = parts[1] if len(parts) > 1 else "main"
            if sub == "how":
                await query.edit_message_text(
                    tr("how_to_play", lang=user_lang),
                    reply_markup=menu_back_keyboard(bot_username, lang=user_lang),
                    parse_mode="Markdown",
                )
            elif sub == "tips":
                await query.edit_message_text(
                    tr("question_tips", lang=user_lang),
                    reply_markup=menu_back_keyboard(bot_username, lang=user_lang),
                    parse_mode="Markdown",
                )
            elif sub == "locs":
                locs = get_locations(user_lang)
                formatted = [
                    f"{format_location(name)}: _{', '.join(roles)}_"
                    for name, roles in locs.items()
                ]
                await query.edit_message_text(
                    tr("locations", lang=user_lang, names="\n".join(formatted)),
                    reply_markup=menu_back_keyboard(bot_username, lang=user_lang),
                    parse_mode="Markdown",
                )
            elif sub == "lang_menu":
                await query.edit_message_text(
                    tr("choose_lang", lang=user_lang),
                    reply_markup=menu_lang_keyboard(bot_username, lang=user_lang),
                    parse_mode="Markdown",
                )
            elif sub == "set_lang":
                new_lang = parts[2] if len(parts) > 2 else "uz"
                if new_lang not in ("uz", "ru"):
                    new_lang = "uz"
                if hasattr(svc.storage, "set_user_lang"):
                    svc.storage.set_user_lang(user_id, new_lang)
                user_lang = new_lang
                lang_name = tr(f"lang_{new_lang}", lang=new_lang)
                try:
                    await query.answer(
                        tr("user_lang_changed", lang=new_lang, lang_name=lang_name)
                    )
                except TelegramError:
                    pass
                await query.edit_message_text(
                    tr("private_start", lang=user_lang),
                    reply_markup=start_menu_keyboard(bot_username, lang=user_lang),
                    parse_mode="Markdown",
                )
            else:
                await query.edit_message_text(
                    tr("private_start", lang=user_lang),
                    reply_markup=start_menu_keyboard(bot_username, lang=user_lang),
                    parse_mode="Markdown",
                )
            return

        # Spy looking up 24 locations in private DM
        if action == "s":
            if update.effective_chat.type != "private":
                return
            chat_id = int(parts[2]) if len(parts) > 2 else None
            sid = parts[3] if len(parts) > 3 else None
            lang = "uz"
            if chat_id:
                game = svc.storage.get(chat_id)
                if game and getattr(game, "sid", None) == sid:
                    lang = getattr(game, "lang", "uz")
                elif hasattr(svc.storage, "get_chat_lang"):
                    lang = svc.storage.get_chat_lang(chat_id) or "uz"
            if not lang and hasattr(svc.storage, "get_user_lang"):
                lang = svc.storage.get_user_lang(update.effective_user.id) or "uz"

            locs = get_locations(lang)
            formatted = [
                f"{format_location(name)}: _{', '.join(roles)}_"
                for name, roles in locs.items()
            ]
            text = tr("locations", lang=lang, names="\n".join(formatted))
            await query.message.reply_text(text, parse_mode="Markdown")
            return

        # Lobby interactive buttons
        if action == "l":
            if update.effective_chat.type not in ("group", "supergroup"):
                raise GameError("group_only")
            sub = parts[1]
            sid = parts[2]
            chat_id = update.effective_chat.id
            async with svc.locks.for_chat(chat_id):
                game = svc.storage.get(chat_id)
                if not game or game.sid != sid:
                    raise GameError("stale")
                await svc.expire(game)
                if svc.storage.get(chat_id) is None:
                    raise GameError("stale")
                if sub == "leave":
                    await remove_player(svc, game, update.effective_user.id)
                elif sub == "start":
                    game.deal(update.effective_user.id)
                    svc.storage.save(game)
                    await svc.distribute(game)
                elif sub == "rules":
                    lang = getattr(game, "lang", "uz")
                    if lang == "ru":
                        popup = (
                            "🕵️ Правила Шпиона:\n"
                            "• 1 шпион, остальные в одной секретной локации.\n"
                            "• Задавайте вопросы по очереди, не выдавая локацию!\n"
                            "• При подозрении используйте /accuse."
                        )
                    else:
                        popup = (
                            "🕵️ Shpion qoidalari:\n"
                            "• 1 kishi shpion, boshqalar bitta maxfiy joyda.\n"
                            "• Navbat bilan savol bering, joy nomini aytmang!\n"
                            "• Gumon bo‘lsa /accuse bilan ayblang."
                        )
                    try:
                        await query.answer(popup, show_alert=True)
                    except TelegramError:
                        pass
                elif sub == "time_menu":
                    await require_manager(update, context, game)
                    await svc.edit(
                        chat_id,
                        game.lobby_message_id,
                        svc.render_lobby(game),
                        reply_markup=lobby_time_keyboard(game),
                        parse_mode="Markdown",
                    )
                elif sub == "time":
                    await require_manager(update, context, game)
                    minutes = int(parts[3])
                    game.minutes = minutes
                    svc.storage.save(game)
                    await svc.update_lobby(game)
                elif sub == "lang_menu":
                    await require_manager(update, context, game)
                    await svc.edit(
                        chat_id,
                        game.lobby_message_id,
                        svc.render_lobby(game),
                        reply_markup=lobby_lang_keyboard(game),
                        parse_mode="Markdown",
                    )
                elif sub == "set_lang":
                    await require_manager(update, context, game)
                    new_lang = parts[3] if len(parts) > 3 else "uz"
                    if new_lang not in ("uz", "ru"):
                        new_lang = "uz"
                    game.set_language(new_lang)
                    if hasattr(svc.storage, "set_chat_lang"):
                        svc.storage.set_chat_lang(chat_id, new_lang)
                    svc.storage.save(game)
                    await svc.update_lobby(game)
                elif sub == "back":
                    await svc.update_lobby(game)
            return

        # Existing actions: g (guess), j (join), a (accuse), v (vote)
        if action == "g" and len(parts) == 4:
            if update.effective_chat.type != "private":
                raise GameError("stale")
            chat_id, sid, value = int(parts[1]), parts[2], int(parts[3])
        elif action in ("j", "a", "v"):
            if update.effective_chat.type not in ("group", "supergroup"):
                raise GameError("group_only")
            if len(parts) != (2 if action == "j" else 3):
                raise GameError("stale")
            chat_id, sid = update.effective_chat.id, parts[1]
            value = int(parts[2]) if len(parts) == 3 else None
        else:
            raise GameError("stale")

        async with svc.locks.for_chat(chat_id):
            game = svc.storage.get(chat_id)
            if not game or game.sid != sid:
                raise GameError("stale")
            await svc.expire(game)
            if svc.storage.get(chat_id) is None:
                raise GameError("stale")
            uid = update.effective_user.id
            if action == "j":
                await add_player(svc, game, update.effective_user)
            elif action == "a":
                await begin_vote(svc, game, uid, value)
            elif action == "v":
                if value not in (0, 1):
                    raise GameError("stale")
                lang = getattr(game, "lang", "uz")
                complete = game.vote(uid, bool(value), svc.clock())
                svc.storage.save(game)
                try:
                    await query.answer(tr("voted", lang=lang))
                except TelegramError:
                    pass
                if complete:
                    await svc.resolve_vote(game)
            elif action == "g":
                lang = getattr(game, "lang", "uz")
                game.guess(uid, value, svc.clock())
                svc.storage.save(game)
                await svc.publish_result(game)
                try:
                    await query.edit_message_text(tr("guess_saved", lang=lang))
                except TelegramError:
                    pass
    except (GameError, ValueError, IndexError) as exc:
        key = str(exc) if isinstance(exc, GameError) else "stale"
        err_lang = "uz"
        if update.effective_chat:
            if update.effective_chat.type == "private":
                if hasattr(svc.storage, "get_user_lang") and update.effective_user:
                    err_lang = (
                        svc.storage.get_user_lang(update.effective_user.id)
                        or "uz"
                    )
            else:
                if hasattr(svc.storage, "get_chat_lang"):
                    err_lang = (
                        svc.storage.get_chat_lang(update.effective_chat.id)
                        or "uz"
                    )
        try:
            await query.answer(tr(key, lang=err_lang), show_alert=True)
        except TelegramError:
            await svc.send(update.effective_chat.id, tr(key, lang=err_lang))

