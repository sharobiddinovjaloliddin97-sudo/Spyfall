from game import Game, GameError, Phase
from handlers.common import (
    current,
    group_command,
    player,
    require_manager,
    service,
)
from keyboards import lobby_keyboard
from texts import tr


@group_command
async def newgame(update, context):
    svc = service(context)
    chat = update.effective_chat
    if svc.storage.get(chat.id):
        raise GameError("exists")
    game = Game(
        chat.id, (chat.title or str(chat.id))[:100], update.effective_user.id
    )
    svc.storage.save(game)
    sent = await svc.send(
        chat.id,
        tr(
            "lobby",
            name=update.effective_user.full_name,
        ),
        reply_markup=lobby_keyboard(game, context.bot.username),
    )
    if sent is None:
        svc.storage.delete(chat.id, game.sid)


async def add_player(svc, game, user):
    new_player = player(user)
    game.join(new_player)
    svc.storage.save(game)
    await svc.send(
        game.chat_id,
        tr(
            "joined",
            name=new_player.name,
            count=len(game.players),
        ),
    )


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
    uid = update.effective_user.id
    game.leave(uid)
    svc.storage.save(game)
    await svc.send(
        game.chat_id,
        tr(
            "left",
            name=update.effective_user.full_name,
            count=len(game.players),
        ),
    )


@group_command
async def players(update, context):
    game = current(service(context), update.effective_chat.id)
    names = "\n".join(
        f"{i}. {p.name}" + (f" (@{p.username})" if p.username else "")
        for i, p in enumerate(game.players.values(), 1)
    ) or tr("empty")
    await update.message.reply_text(
        tr(
            "players",
            count=len(game.players),
            names=names,
            minutes=game.minutes,
        )
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
    await update.message.reply_text(tr("time_set", minutes=minutes))
