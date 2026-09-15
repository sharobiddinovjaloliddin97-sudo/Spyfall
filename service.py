"""Telegram side effects and timers. Call game methods under the chat lock."""

import logging
import math
import time

from telegram.error import TelegramError

from game import Phase
from keyboards import guess_keyboard, lobby_keyboard, spy_role_keyboard
from locations import format_location
from storage import ChatLocks, Storage
from texts import tr

LOG = logging.getLogger(__name__)


class GameService:
    def __init__(self, application, storage: Storage, clock=time.monotonic):
        self.app = application
        self.storage = storage
        self.clock = clock
        self.locks = ChatLocks()

    async def send(self, chat_id, text, **kwargs):
        try:
            return await self.app.bot.send_message(chat_id, text, **kwargs)
        except TelegramError as exc:
            # Never log tokens, API URLs, role messages, or raw exceptions.
            LOG.warning("Xabar yuborilmadi (%s).", type(exc).__name__)
            return None

    async def edit(self, chat_id, message_id, text, **kwargs):
        try:
            return await self.app.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                **kwargs,
            )
        except TelegramError as exc:
            LOG.warning("Xabar tahrirlanmadi (%s).", type(exc).__name__)
            return None

    def render_lobby(self, game):
        if not game.players:
            player_list = tr("empty")
        else:
            player_list = "\n".join(
                f"{i}. 👤 {p.name}" + (f" (@{p.username})" if p.username else "")
                for i, p in enumerate(game.players.values(), 1)
            )
        status_hint = (
            tr("lobby_waiting")
            if len(game.players) < 3
            else tr("lobby_ready")
        )
        creator_name = (
            game.players[game.owner_id].name
            if game.owner_id in game.players
            else str(game.owner_id)
        )
        return tr(
            "lobby",
            name=creator_name,
            minutes=game.minutes,
            count=len(game.players),
            player_list=player_list,
            status_hint=status_hint,
        )

    async def update_lobby(self, game):
        text = self.render_lobby(game)
        bot_username = getattr(self.app.bot, "username", None) or "SpyfallBot"
        markup = lobby_keyboard(game, bot_username)
        if game.lobby_message_id:
            res = await self.edit(
                game.chat_id,
                game.lobby_message_id,
                text,
                reply_markup=markup,
                parse_mode="Markdown",
            )
            if res:
                return res
        sent = await self.send(
            game.chat_id,
            text,
            reply_markup=markup,
            parse_mode="Markdown",
        )
        if sent:
            game.lobby_message_id = sent.message_id
            self.storage.save(game)
        return sent

    def schedule(self, game, event, delay):
        self.app.job_queue.run_once(
            self.on_timer,
            max(0.01, delay),
            data=(game.chat_id, game.sid, event),
            name=f"{game.chat_id}:{game.sid}:{event}",
        )

    def cancel_jobs(self, game):
        prefix = f"{game.chat_id}:{game.sid}:"
        for job in self.app.job_queue.jobs():
            if job.name and job.name.startswith(prefix):
                job.schedule_removal()

    async def cancel(self, game):
        self.cancel_jobs(game)
        self.storage.delete(game.chat_id, game.sid)
        game.phase = Phase.ENDED
        await self.send(game.chat_id, tr("cancelled"), parse_mode="Markdown")

    async def distribute(self, game):
        # Probe all DMs first, before disclosing any roles.
        failed = []
        for uid, player in game.players.items():
            sent = await self.send(
                uid, tr("probe", group=game.title), parse_mode="Markdown"
            )
            if sent is None:
                failed.append(player.name)
        if not failed:
            for uid, player in game.players.items():
                if uid == game.spy_id:
                    message = tr("spy_role", group=game.title, sid=game.sid)
                    markup = spy_role_keyboard(game.chat_id, game.sid)
                else:
                    message = tr(
                        "role",
                        group=game.title,
                        sid=game.sid,
                        location=format_location(game.location),
                        role=game.roles[uid],
                    )
                    markup = None
                if (
                    await self.send(
                        uid,
                        message,
                        parse_mode="Markdown",
                        reply_markup=markup,
                    )
                    is None
                ):
                    failed.append(player.name)
        if failed:
            game.reset_lobby()
            self.storage.save(game)
            await self.send(
                game.chat_id,
                tr("dm_failed", names=", ".join(failed)),
                parse_mode="Markdown",
            )
            await self.update_lobby(game)
            return
        game.activate(self.clock())
        self.storage.save(game)
        duration = game.minutes * 60
        self.schedule(game, "end", duration)
        self.schedule(game, "half", duration / 2)
        if duration / 2 != duration - 60:
            self.schedule(game, "minute", duration - 60)
        first_player = (
            game.players[game.first_player_id].name
            if game.first_player_id in game.players
            else "Ishtirokchilardan biri"
        )
        sent = await self.send(
            game.chat_id,
            tr("started", minutes=game.minutes, first_player=first_player),
            parse_mode="Markdown",
        )
        if sent is None:
            await self.cancel(game)

    async def publish_result(self, game):
        self.cancel_jobs(game)
        # Commit once before sending the result; failed Telegram sends cannot
        # produce duplicate statistics or keep a finished game active.
        self.storage.record(game)
        self.storage.delete(game.chat_id, game.sid)
        await self.send(
            game.chat_id,
            tr(
                "result",
                spy=game.players[game.spy_id].name,
                location=format_location(game.location),
                winner=tr(f"{game.winner}_winner"),
                reason=tr(game.reason),
            ),
            parse_mode="Markdown",
        )

    async def resolve_vote(self, game):
        yes = sum(game.votes.values())
        no = len(game.votes) - yes
        game.resolve_vote(self.clock())
        self.storage.save(game)
        await self.send(
            game.chat_id,
            tr(
                "vote_result",
                yes=yes,
                no=no,
                absent=len(game.players) - len(game.votes),
            ),
            parse_mode="Markdown",
        )
        if game.phase == Phase.ENDED:
            await self.publish_result(game)
            return
        # The round timer no longer applies during the final chance.
        self.cancel_jobs(game)
        await self.send(game.chat_id, tr("last_chance"), parse_mode="Markdown")
        sent = await self.send(
            game.spy_id,
            tr("guess_prompt", group=game.title),
            reply_markup=guess_keyboard(game),
            parse_mode="Markdown",
        )
        if sent is None:
            game.finish("civilians", "guess_dm_failed_reason")
            await self.publish_result(game)
            return
        # Give the spy a full 30 seconds after delivery.
        game.guess_deadline = self.clock() + 30
        self.storage.save(game)
        self.schedule(game, "guess", 30)

    async def expire(self, game):
        """Enforce deadlines even if the scheduler is delayed."""
        now = self.clock()
        if game.phase == Phase.ACTIVE and now >= game.deadline:
            game.finish("spy", "timeout_reason")
            await self.publish_result(game)
        elif game.phase == Phase.VOTING and now >= game.vote_deadline:
            await self.resolve_vote(game)
        elif game.phase == Phase.GUESS and now >= game.guess_deadline:
            game.finish("civilians", "guess_timeout_reason")
            await self.publish_result(game)

    async def on_timer(self, context):
        chat_id, sid, event = context.job.data
        async with self.locks.for_chat(chat_id):
            game = self.storage.get(chat_id)
            if not game or game.sid != sid:
                return
            await self.expire(game)
            if self.storage.get(chat_id) is None:
                return
            if event in ("half", "minute") and game.phase == Phase.ACTIVE:
                remaining = max(
                    1,
                    math.ceil(
                        (game.deadline - self.clock()) / 60,
                    ),
                )
                await self.send(chat_id, tr("reminder", minutes=remaining))
            deadlines = {
                "end": (Phase.ACTIVE, game.deadline),
                "vote": (Phase.VOTING, game.vote_deadline),
                "guess": (Phase.GUESS, game.guess_deadline),
            }
            # Handles an early scheduler callback without losing expiry.
            if event in deadlines:
                phase, deadline = deadlines[event]
                if game.phase == phase and self.clock() < deadline:
                    self.schedule(game, event, deadline - self.clock())
