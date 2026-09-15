from handlers.common import current, group_command, require_manager, service
from locations import LOCATIONS
from texts import tr


async def start(update, context):
    key = (
        "private_start"
        if update.effective_chat.type == "private"
        else "group_start"
    )
    await update.effective_message.reply_text(tr(key))


async def help_command(update, context):
    await update.effective_message.reply_text(tr("help"))


async def locations(update, context):
    await update.effective_message.reply_text(
        tr(
            "locations",
            names="\n".join(LOCATIONS),
        )
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
            )
        )
