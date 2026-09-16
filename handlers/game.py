from game import Phase
from handlers.common import current, group_command, require_manager, service
from keyboards import (
    lobby_lang_keyboard,
    menu_lang_keyboard,
    start_menu_keyboard,
)
from locations import format_location, get_locations
from texts import tr


async def start(update, context):
    svc = service(context)
    if update.effective_chat.type == "private":
        user = update.effective_user
        user_lang = None
        if hasattr(svc.storage, "get_user_lang"):
            user_lang = svc.storage.get_user_lang(user.id)
        if not user_lang:
            user_lang = (
                "ru"
                if (user.language_code or "").lower().startswith("ru")
                else "uz"
            )
            if hasattr(svc.storage, "set_user_lang"):
                svc.storage.set_user_lang(user.id, user_lang)
        bot_username = getattr(context.bot, "username", None) or "SpyfallBot"
        await update.effective_message.reply_text(
            tr("private_start", lang=user_lang),
            reply_markup=start_menu_keyboard(bot_username, lang=user_lang),
            parse_mode="Markdown",
        )
    else:
        chat_lang = "uz"
        if hasattr(svc.storage, "get_chat_lang"):
            chat_lang = svc.storage.get_chat_lang(update.effective_chat.id)
        await update.effective_message.reply_text(
            tr("group_start", lang=chat_lang),
            parse_mode="Markdown",
        )


async def help_command(update, context):
    svc = service(context)
    lang = "uz"
    if update.effective_chat.type == "private":
        if hasattr(svc.storage, "get_user_lang"):
            lang = svc.storage.get_user_lang(update.effective_user.id) or "uz"
    else:
        if hasattr(svc.storage, "get_chat_lang"):
            lang = svc.storage.get_chat_lang(update.effective_chat.id) or "uz"
        game = svc.storage.get(update.effective_chat.id)
        if game:
            lang = getattr(game, "lang", lang)
    await update.effective_message.reply_text(
        tr("help", lang=lang),
        parse_mode="Markdown",
    )


async def locations(update, context):
    svc = service(context)
    lang = "uz"
    if update.effective_chat.type == "private":
        if hasattr(svc.storage, "get_user_lang"):
            lang = svc.storage.get_user_lang(update.effective_user.id) or "uz"
    else:
        if hasattr(svc.storage, "get_chat_lang"):
            lang = svc.storage.get_chat_lang(update.effective_chat.id) or "uz"
        game = svc.storage.get(update.effective_chat.id)
        if game:
            lang = getattr(game, "lang", lang)

    locs = get_locations(lang)
    formatted = [
        f"{format_location(name)}: _{', '.join(roles)}_"
        for name, roles in locs.items()
    ]
    await update.effective_message.reply_text(
        tr(
            "locations",
            lang=lang,
            names="\n".join(formatted),
        ),
        parse_mode="Markdown",
    )


async def lang_command(update, context):
    svc = service(context)
    bot_username = getattr(context.bot, "username", None) or "SpyfallBot"
    if update.effective_chat.type == "private":
        user_lang = "uz"
        if hasattr(svc.storage, "get_user_lang"):
            user_lang = svc.storage.get_user_lang(update.effective_user.id) or "uz"
        await update.effective_message.reply_text(
            tr("choose_lang", lang=user_lang),
            reply_markup=menu_lang_keyboard(bot_username, lang=user_lang),
            parse_mode="Markdown",
        )
    else:
        chat_lang = "uz"
        if hasattr(svc.storage, "get_chat_lang"):
            chat_lang = svc.storage.get_chat_lang(update.effective_chat.id) or "uz"
        game = svc.storage.get(update.effective_chat.id)
        if game:
            chat_lang = getattr(game, "lang", chat_lang)

        if context.args:
            target = context.args[0].lower()
            if target in ("uz", "uzbek", "o'zbek", "ozbek"):
                new_lang = "uz"
            elif target in ("ru", "rus", "russian", "русский"):
                new_lang = "ru"
            else:
                await update.effective_message.reply_text(
                    "Namuna / Пример: `/lang uz` yoki `/lang ru`",
                    parse_mode="Markdown",
                )
                return

            user_id = update.effective_user.id
            is_admin = False
            try:
                member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
                if member.status in ("creator", "administrator"):
                    is_admin = True
            except Exception:
                pass
            if game and game.owner_id == user_id:
                is_admin = True

            if not is_admin:
                await update.effective_message.reply_text(
                    tr("owner_only", lang=chat_lang),
                    parse_mode="Markdown",
                )
                return

            if hasattr(svc.storage, "set_chat_lang"):
                svc.storage.set_chat_lang(update.effective_chat.id, new_lang)
            if game:
                game.set_language(new_lang)
                svc.storage.save(game)
                await svc.update_lobby(game)
            lang_name = tr(f"lang_{new_lang}", lang=new_lang)
            await update.effective_message.reply_text(
                tr("lang_changed", lang=new_lang, lang_name=lang_name),
                parse_mode="Markdown",
            )
        else:
            if game and game.phase == Phase.LOBBY:
                await update.effective_message.reply_text(
                    tr("choose_lang", lang=chat_lang),
                    reply_markup=lobby_lang_keyboard(game),
                    parse_mode="Markdown",
                )
            else:
                label = "🇺🇿 O‘zbekcha" if chat_lang == "uz" else "🇷🇺 Русский"
                await update.effective_message.reply_text(
                    f"🌐 Guruh tili / Язык группы: {label}\n\nO‘zgartirish uchun / Для смены: `/lang uz` yoki `/lang ru`",
                    parse_mode="Markdown",
                )


@group_command
async def startgame(update, context):
    svc = service(context)
    game = current(svc, update.effective_chat.id)
    game.deal(update.effective_user.id)
    svc.storage.save(game)
    await svc.distribute(game)


@group_command
async def endgame(update, context):
    svc = service(context)
    game = current(svc, update.effective_chat.id)
    await require_manager(update, context, game)
    await svc.cancel(game)


@group_command
async def stats(update, context):
    svc = service(context)
    game = svc.storage.get(update.effective_chat.id)
    chat_lang = "uz"
    if hasattr(svc.storage, "get_chat_lang"):
        chat_lang = svc.storage.get_chat_lang(update.effective_chat.id) or "uz"
    lang = getattr(game, "lang", chat_lang)
    rows = svc.storage.stats(update.effective_chat.id)
    if not rows:
        await update.message.reply_text(tr("stats_empty", lang=lang))
        return
    # Page long group rankings to stay within Telegram message limits.
    for offset in range(0, len(rows), 15):
        await update.message.reply_text(
            tr(
                "stats",
                lang=lang,
                rows="\n".join(
                    tr(
                        "stats_row",
                        lang=lang,
                        name=s.name,
                        games=s.games,
                        spy=s.spy,
                        wins=s.wins,
                    )
                    for s in rows[offset : offset + 15]
                ),
            ),
            parse_mode="Markdown",
        )

