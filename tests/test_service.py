import asyncio
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from telegram.error import Forbidden

from game import Game, Phase, Player
from handlers.voting import callback
from keyboards import guess_keyboard
from main import build_application
from service import GameService
from storage import MemoryStorage
from tests.test_game import active_game


class Queue:
    def __init__(self):
        self.items = []

    def run_once(self, callback, delay, data, name):
        job = SimpleNamespace(
            callback=callback,
            delay=delay,
            data=data,
            name=name,
            removed=False,
        )
        job.schedule_removal = lambda: setattr(job, "removed", True)
        self.items.append(job)

    def jobs(self):
        return [job for job in self.items if not job.removed]


class ServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.now = 100
        self.bot = SimpleNamespace(
            send_message=AsyncMock(
                return_value=SimpleNamespace(message_id=1),
            ),
            edit_message_text=AsyncMock(
                return_value=SimpleNamespace(message_id=1),
            ),
        )
        self.app = SimpleNamespace(
            bot=self.bot, job_queue=Queue(), bot_data={}
        )
        self.svc = GameService(self.app, MemoryStorage(), lambda: self.now)
        self.app.bot_data["service"] = self.svc

    def pending_game(self):
        game = Game(-100, "Guruh", 1)
        for uid in (1, 2, 3):
            game.join(Player(uid, f"Ism {uid}"))
        game.deal(1)
        self.svc.storage.save(game)
        return game

    async def test_distribution_secrets_and_timer_schedule(self):
        game = self.pending_game()
        await self.svc.distribute(game)
        self.assertEqual(game.phase, Phase.ACTIVE)
        calls = self.bot.send_message.call_args_list
        group_text = " ".join(c.args[1] for c in calls if c.args[0] < 0)
        self.assertNotIn(game.location, group_text)
        role_calls = calls[3:6]
        self.assertEqual(len(role_calls), 3)
        for call in role_calls:
            if call.args[0] == game.spy_id:
                self.assertIn("SHPIONSIZ", call.args[1])
                self.assertNotIn(game.location, call.args[1])
            else:
                self.assertIn(game.location, call.args[1])
        self.assertEqual(
            sorted(job.delay for job in self.app.job_queue.jobs()),
            [240, 420, 480],
        )

    async def test_dm_failure_aborts_without_any_role_leak(self):
        game = self.pending_game()

        async def send(chat_id, text, **kwargs):
            if chat_id == 2:
                raise Forbidden("blocked")
            return SimpleNamespace(message_id=1)

        self.bot.send_message.side_effect = send
        await self.svc.distribute(game)
        self.assertEqual(game.phase, Phase.LOBBY)
        self.assertIsNone(game.location)
        self.assertIsNone(game.spy_id)
        self.assertEqual(game.roles, {})
        self.assertEqual(self.svc.storage.stats(game.chat_id), [])
        self.assertEqual(self.app.job_queue.jobs(), [])
        self.assertFalse(
            any(
                "Rolingiz:" in c.args[1] or "SHPIONSIZ" in c.args[1]
                for c in self.bot.send_message.call_args_list
            )
        )
        self.assertIn("Ism 2", self.bot.send_message.call_args_list[4].args[1])

    async def test_partial_role_delivery_aborts_without_statistics(self):
        game = self.pending_game()

        async def send(chat_id, text, **kwargs):
            if chat_id == 3 and "🔑" in text:
                raise Forbidden("blocked after probe")
            return SimpleNamespace(message_id=1)

        self.bot.send_message.side_effect = send
        await self.svc.distribute(game)
        self.assertEqual(game.phase, Phase.LOBBY)
        self.assertIsNone(game.location)
        self.assertIsNone(game.spy_id)
        self.assertEqual(self.app.job_queue.jobs(), [])
        self.assertEqual(self.svc.storage.stats(game.chat_id), [])

    async def test_timeout_and_duplicate_job_do_not_double_count(self):
        game = active_game()
        self.svc.storage.save(game)
        self.now = game.deadline
        ctx = SimpleNamespace(
            job=SimpleNamespace(
                data=(game.chat_id, game.sid, "end"),
            )
        )
        await asyncio.gather(self.svc.on_timer(ctx), self.svc.on_timer(ctx))
        self.assertIsNone(self.svc.storage.get(game.chat_id))
        self.assertEqual(self.bot.send_message.await_count, 1)
        self.assertEqual(sum(s.games for s in self.svc.storage.stats(-100)), 3)

    async def test_old_job_does_not_touch_new_lobby(self):
        game = Game(-100, "Yangi", 1)
        self.svc.storage.save(game)
        await self.svc.on_timer(
            SimpleNamespace(
                job=SimpleNamespace(
                    data=(-100, "old-sid", "end"),
                )
            )
        )
        self.assertEqual(game.phase, Phase.LOBBY)
        self.bot.send_message.assert_not_awaited()

    async def test_caught_spy_guess_timeout_and_cancel(self):
        game = active_game()
        self.svc.storage.save(game)
        accuser = next(uid for uid in game.players if uid != game.spy_id)
        game.accuse(accuser, game.spy_id, 101)
        for uid in game.players:
            game.vote(uid, True, 102)
        self.now = 102
        await self.svc.resolve_vote(game)
        self.assertEqual(game.phase, Phase.GUESS)
        self.assertEqual(len(self.app.job_queue.jobs()), 1)
        self.now = game.guess_deadline
        await self.svc.expire(game)
        self.assertEqual(game.winner, "civilians")
        self.assertIsNone(self.svc.storage.get(game.chat_id))
        self.assertEqual(self.app.job_queue.jobs(), [])
        game = active_game(-200)
        self.svc.storage.save(game)
        self.svc.schedule(game, "end", 480)
        await self.svc.cancel(game)
        self.assertEqual(self.svc.storage.stats(-200), [])
        self.assertEqual(self.app.job_queue.jobs(), [])

    def query(self, data, uid, chat_id=-100, private=False):
        query = SimpleNamespace(
            data=data,
            answer=AsyncMock(),
            edit_message_text=AsyncMock(),
            message=SimpleNamespace(
                reply_text=AsyncMock(),
            ),
        )
        bot = SimpleNamespace(
            username="TestSpyfallBot",
            get_chat_member=AsyncMock(
                return_value=SimpleNamespace(status="administrator")
            ),
        )
        update = SimpleNamespace(
            callback_query=query,
            effective_chat=SimpleNamespace(
                id=chat_id,
                type="private" if private else "supergroup",
            ),
            effective_user=SimpleNamespace(
                id=uid, full_name=f"User {uid}", username=f"user{uid}"
            ),
        )
        return update, SimpleNamespace(application=self.app, bot=bot)

    async def test_private_menu_navigation(self):
        update, ctx = self.query("m:how", 1, 1, private=True)
        await callback(update, ctx)
        update.callback_query.edit_message_text.assert_awaited()
        self.assertIn("QANDAY O‘YNALADI", update.callback_query.edit_message_text.call_args[0][0])

        update, ctx = self.query("m:tips", 1, 1, private=True)
        await callback(update, ctx)
        self.assertIn("MASLAHATLAR", update.callback_query.edit_message_text.call_args[0][0])

        update, ctx = self.query("m:locs", 1, 1, private=True)
        await callback(update, ctx)
        self.assertIn("Barcha mumkin", update.callback_query.edit_message_text.call_args[0][0])

    async def test_spy_locations_callback(self):
        update, ctx = self.query("s:locs:-100:test-sid", 1, 1, private=True)
        await callback(update, ctx)
        update.callback_query.message.reply_text.assert_awaited()
        self.assertIn("Barcha mumkin", update.callback_query.message.reply_text.call_args[0][0])

    async def test_lobby_interactive_callbacks(self):
        game = Game(-100, "Guruh", 1)
        game.join(Player(1, "User 1"))
        game.join(Player(2, "User 2"))
        self.svc.storage.save(game)

        # Leave callback
        update, ctx = self.query(f"l:leave:{game.sid}", 2)
        await callback(update, ctx)
        self.assertNotIn(2, game.players)

        # Re-join via j:
        update, ctx = self.query(f"j:{game.sid}", 2)
        await callback(update, ctx)
        self.assertIn(2, game.players)

        # Time change via l:time:
        update, ctx = self.query(f"l:time:{game.sid}:10", 1)
        await callback(update, ctx)
        self.assertEqual(game.minutes, 10)

        # Rules popup
        update, ctx = self.query(f"l:rules:{game.sid}", 1)
        await callback(update, ctx)
        update.callback_query.answer.assert_awaited()

    async def test_callbacks_stale_unauthorized_and_concurrent_votes(self):
        game = active_game()
        self.svc.storage.save(game)
        game.accuse(1, 2, 101)
        self.now = 102
        update, ctx = self.query(f"v:{game.sid}:1", 999)
        await callback(update, ctx)
        self.assertEqual(game.votes, {})
        update, ctx = self.query("v:old-sid:1", 1)
        await callback(update, ctx)
        self.assertEqual(game.votes, {})
        update, ctx = self.query(f"v:{game.sid}:1", 1)
        await asyncio.gather(callback(update, ctx), callback(update, ctx))
        self.assertEqual(game.votes, {1: True})

    async def test_private_guess_bound_to_spy_and_session(self):
        game = active_game()
        game.phase = Phase.GUESS
        game.guess_deadline = 130
        self.svc.storage.save(game)
        index = game.locations.index(game.location)
        data = f"g:{game.chat_id}:{game.sid}:{index}"
        update, ctx = self.query(data, 999, 999, private=True)
        await callback(update, ctx)
        self.assertEqual(game.phase, Phase.GUESS)
        update, ctx = self.query(data, game.spy_id, game.spy_id, private=True)
        await asyncio.gather(callback(update, ctx), callback(update, ctx))
        self.assertEqual(game.winner, "spy")
        self.assertEqual(sum(s.wins for s in self.svc.storage.stats(-100)), 1)

    def test_keyboard_payload_size_and_app_wiring(self):
        game = active_game(-1001234567890)
        for row in guess_keyboard(game).inline_keyboard:
            for button in row:
                self.assertLessEqual(len(button.callback_data.encode()), 64)
        # This construction-only test must not depend on host proxy settings.
        clean_env = {
            key: value
            for key, value in os.environ.items()
            if not key.lower().endswith("_proxy")
        }
        with patch.dict(os.environ, clean_env, clear=True):
            app = build_application("123456789:ABC_test_token")
        self.assertIsNotNone(app.job_queue)
        commands = set()
        for handler in app.handlers[0]:
            commands.update(getattr(handler, "commands", []))
        self.assertTrue(
            {
                "start",
                "help",
                "newgame",
                "join",
                "leave",
                "players",
                "settime",
                "startgame",
                "endgame",
                "accuse",
                "stats",
            }.issubset(commands)
        )

