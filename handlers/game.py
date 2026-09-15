from handlers.common import current, group_command, require_manager, service
from keyboards import start_menu_keyboard
from locations import LOCATIONS, format_location
from texts import tr


async def start(update, context):
    if update.effective_chat.type == "private":
        await update.effective_message.reply_text(
            tr("private_start"),
            reply_markup=start_menu_keyboard(context.bot.username),
            parse_mode="Markdown",
        )
    else:
        await update.effective_message.reply_text(
            tr("group_start"),
            parse_mode="Markdown",
        )


async def help_command(update, context):
    await update.effective_message.reply_text(
        tr("help"),
        parse_mode="Markdown",
    )


async def locations(update, context):
    formatted = [
        f"{format_location(name)}: _{', '.join(roles)}_"
        for name, roles in LOCATIONS.items()
    ]
    await update.effective_message.reply_text(
        tr(
            "locations",
            names="\n".join(formatted),
        ),
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
    rows = service(context).storage.stats(update.effective_chat.id)
    if not rows:
        await update.message.reply_text(tr("stats_empty"))
        return
    # Page long group rankings to stay within Telegram message limits.
    for offset in range(0, len(rows), 15):
        await update.message.reply_text(
            tr(
                "stats",
                rows="\n".join(
                    tr(
                        "stats_row",
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

