from telegram.error import TelegramError

from game import GameError, Phase
from handlers.common import current, group_command, service
from handlers.lobby import add_player
from keyboards import accuse_keyboard, vote_keyboard
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
    # Acknowledge promptly, including slow role/timer side effects below.
    try:
        await query.answer()
    except TelegramError:
        pass
    svc = service(context)
    try:
        parts = (query.data or "").split(":")
        action = parts[0]
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
                # No extra group messages per vote; answer privately via alert.
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
