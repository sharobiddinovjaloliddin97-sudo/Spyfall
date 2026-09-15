"""Telegram side effects and timers. Call game methods under the chat lock."""

import logging
import math
import time

from telegram.error import TelegramError

from game import Phase
from keyboards import guess_keyboard
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
        await self.send(game.chat_id, tr("cancelled"))

    async def distribute(self, game):
        # Probe all DMs first, before disclosing any roles.
        failed = []
        for uid, player in game.players.items():
            sent = await self.send(uid, tr("probe", group=game.title))
            if sent is None:
                failed.append(player.name)
        if not failed:
            for uid, player in game.players.items():
                if uid == game.spy_id:
                    message = tr("spy_role", group=game.title, sid=game.sid)
                else:
                    message = tr(
                        "role",
                        group=game.title,
                        sid=game.sid,
                        location=game.location,
                        role=game.roles[uid],
                    )
                if await self.send(uid, message) is None:
                    failed.append(player.name)
        if failed:
            self.storage.delete(game.chat_id, game.sid)
            game.phase = Phase.ENDED
            await self.send(
                game.chat_id,
                tr("dm_failed", names=", ".join(failed)),
            )
            return
        game.activate(self.clock())
        self.storage.save(game)
        duration = game.minutes * 60
        self.schedule(game, "end", duration)
        self.schedule(game, "half", duration / 2)
        if duration / 2 != duration - 60:
            self.schedule(game, "minute", duration - 60)
        sent = await self.send(
            game.chat_id,
            tr("started", minutes=game.minutes),
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
                location=game.location,
                winner=tr(f"{game.winner}_winner"),
                reason=tr(game.reason),
            ),
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
        )
        if game.phase == Phase.ENDED:
            await self.publish_result(game)
            return
        # The round timer no longer applies during the final chance.
        self.cancel_jobs(game)
        await self.send(game.chat_id, tr("last_chance"))
        sent = await self.send(
            game.spy_id,
            tr("guess_prompt", group=game.title),
            reply_markup=guess_keyboard(game),
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
