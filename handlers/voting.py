from telegram.error import TelegramError

from game import GameError, Phase
from handlers.common import current, group_command, require_manager, service
from handlers.lobby import add_player, remove_player
from keyboards import (
    accuse_keyboard,
    lobby_time_keyboard,
    menu_back_keyboard,
    start_menu_keyboard,
    vote_keyboard,
)
from locations import LOCATIONS, format_location
from texts import tr


async def begin_vote(svc, game, accuser, accused):
    seconds = game.accuse(accuser, accused, svc.clock())
    svc.storage.save(game)
    svc.schedule(game, "vote", game.vote_deadline - svc.clock())
    sent = await svc.send(
        game.chat_id,
        tr(
            "voting",
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
        await update.message.reply_text(
            tr("select_accused"),
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
            bot_username = context.bot.username
            sub = parts[1] if len(parts) > 1 else "main"
            if sub == "how":
                await query.edit_message_text(
                    tr("how_to_play"),
                    reply_markup=menu_back_keyboard(bot_username),
                    parse_mode="Markdown",
                )
            elif sub == "tips":
                await query.edit_message_text(
                    tr("question_tips"),
                    reply_markup=menu_back_keyboard(bot_username),
                    parse_mode="Markdown",
                )
            elif sub == "locs":
                formatted = [
                    f"{format_location(name)}: _{', '.join(roles)}_"
                    for name, roles in LOCATIONS.items()
                ]
                await query.edit_message_text(
                    tr("locations", names="\n".join(formatted)),
                    reply_markup=menu_back_keyboard(bot_username),
                    parse_mode="Markdown",
                )
            else:
                await query.edit_message_text(
                    tr("private_start"),
                    reply_markup=start_menu_keyboard(bot_username),
                    parse_mode="Markdown",
                )
            return

        # Spy looking up 24 locations in private DM
        if action == "s":
            if update.effective_chat.type != "private":
                return
            formatted = [
                f"{format_location(name)}: _{', '.join(roles)}_"
                for name, roles in LOCATIONS.items()
            ]
            text = tr("locations", names="\n".join(formatted))
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
                complete = game.vote(uid, bool(value), svc.clock())
                svc.storage.save(game)
                try:
                    await query.answer(tr("voted"))
                except TelegramError:
                    pass
                if complete:
                    await svc.resolve_vote(game)
            elif action == "g":
                game.guess(uid, value, svc.clock())
                svc.storage.save(game)
                await svc.publish_result(game)
                try:
                    await query.edit_message_text(tr("guess_saved"))
                except TelegramError:
                    pass
    except (GameError, ValueError, IndexError) as exc:
        key = str(exc) if isinstance(exc, GameError) else "stale"
        try:
            await query.answer(tr(key), show_alert=True)
        except TelegramError:
            await svc.send(update.effective_chat.id, tr(key))

