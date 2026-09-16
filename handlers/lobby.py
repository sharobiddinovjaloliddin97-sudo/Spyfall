from game import Game, GameError, Phase
from handlers.common import (
    current,
    group_command,
    player,
    require_manager,
    service,
)
from texts import tr


@group_command
async def newgame(update, context):
    svc = service(context)
    chat = update.effective_chat
    if svc.storage.get(chat.id):
        raise GameError("exists")
    chat_lang = "uz"
    if hasattr(svc.storage, "get_chat_lang"):
        chat_lang = svc.storage.get_chat_lang(chat.id)
    game = Game(
        chat.id,
        (chat.title or str(chat.id))[:100],
        update.effective_user.id,
        lang=chat_lang,
    )
    svc.storage.save(game)
    sent = await svc.update_lobby(game)
    if sent is None:
        svc.storage.delete(chat.id, game.sid)


async def add_player(svc, game, user):
    new_player = player(user)
    game.join(new_player)
    svc.storage.save(game)
    await svc.update_lobby(game)


async def remove_player(svc, game, user_id):
    game.leave(user_id)
    svc.storage.save(game)
    await svc.update_lobby(game)


@group_command
async def join(update, context):
    svc = service(context)
    await add_player(
        svc,
        current(svc, update.effective_chat.id),
        update.effective_user,
    )


@group_command
async def leave(update, context):
    svc = service(context)
    game = current(svc, update.effective_chat.id)
    await remove_player(svc, game, update.effective_user.id)


@group_command
async def players(update, context):
    game = current(service(context), update.effective_chat.id)
    lang = getattr(game, "lang", "uz")
    names = "\n".join(
        f"{i}. 👤 {p.name}" + (f" (@{p.username})" if p.username else "")
        for i, p in enumerate(game.players.values(), 1)
    ) or tr("empty", lang=lang)
    await update.message.reply_text(
        tr(
            "players",
            lang=lang,
            count=len(game.players),
            names=names,
            minutes=game.minutes,
        ),
        parse_mode="Markdown",
    )


@group_command
async def settime(update, context):
    svc = service(context)
    game = current(svc, update.effective_chat.id)
    game.require(Phase.LOBBY, "lobby_only")
    await require_manager(update, context, game)
    try:
        if len(context.args) != 1:
            raise ValueError
        minutes = int(context.args[0])
        if not 2 <= minutes <= 30:
            raise ValueError
    except ValueError:
        raise GameError("time_usage") from None
    game.minutes = minutes
    svc.storage.save(game)
    await svc.update_lobby(game)
    lang = getattr(game, "lang", "uz")
    await update.message.reply_text(tr("time_set", lang=lang, minutes=minutes))

