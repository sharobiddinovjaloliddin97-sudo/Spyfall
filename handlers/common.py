from functools import wraps

from game import GameError, Player
from texts import tr


def service(context):
    return context.application.bot_data["service"]


def player(user):
    return Player(user.id, user.full_name[:80], user.username)


def current(svc, chat_id):
    game = svc.storage.get(chat_id)
    if game is None:
        raise GameError("missing")
    return game


def group_command(func):
    @wraps(func)
    async def wrapped(update, context):
        if update.effective_chat.type not in ("group", "supergroup"):
            await update.effective_message.reply_text(tr("group_only"))
            return
        if (
            not update.effective_user
            or update.effective_user.is_bot
            or update.effective_message.sender_chat
        ):
            await update.effective_message.reply_text(tr("human_only"))
            return
        svc = service(context)
        async with svc.locks.for_chat(update.effective_chat.id):
            game = svc.storage.get(update.effective_chat.id)
            if game:
                await svc.expire(game)
            try:
                await func(update, context)
            except GameError as exc:
                await update.effective_message.reply_text(tr(str(exc)))

    return wrapped


async def require_manager(update, context, game):
    uid = update.effective_user.id
    if uid == game.owner_id:
        return
    member = await context.bot.get_chat_member(game.chat_id, uid)
    if member.status not in ("creator", "administrator"):
        raise GameError("owner_only")
