import random
import unittest

from game import Game, GameError, Phase, Player
from locations import LOCATIONS
from storage import MemoryStorage


def active_game(chat_id=-100, count=3):
    game = Game(chat_id, "Sinov guruhi", 1)
    for uid in range(1, count + 1):
        game.join(Player(uid, f"O‘yinchi {uid}", f"user{uid}"))
    game.deal(1, random.Random(4))
    game.activate(100)
    return game


class RulesTests(unittest.TestCase):
    def test_join_limits_leave_and_minimum(self):
        game = Game(-1, "Guruh", 1)
        game.join(Player(1, "Ali"))
        with self.assertRaisesRegex(GameError, "already_joined"):
            game.join(Player(1, "Ali"))
        with self.assertRaisesRegex(GameError, "minimum"):
            game.deal(1)
        for uid in range(2, 11):
            game.join(Player(uid, str(uid)))
        with self.assertRaisesRegex(GameError, "full"):
            game.join(Player(11, "11"))
        game.leave(10)
        self.assertEqual(len(game.players), 9)
        game.deal(1)
        with self.assertRaisesRegex(GameError, "lobby_only"):
            game.leave(1)

    def test_roles_and_locations(self):
        self.assertGreaterEqual(len(LOCATIONS), 20)
        self.assertTrue(all(LOCATIONS.values()))
        for seed in range(40):
            game = active_game(count=10)
            game.phase = Phase.LOBBY
            game.deal(1, random.Random(seed))
            self.assertIn(game.location, LOCATIONS)
            self.assertNotIn(game.spy_id, game.roles)
            self.assertEqual(len(game.roles), 9)
            self.assertTrue(
                all(
                    role in LOCATIONS[game.location]
                    for role in game.roles.values()
                )
            )

    def test_accusation_and_vote_guards(self):
        game = active_game()
        with self.assertRaisesRegex(GameError, "not_player"):
            game.accuse(55, 1, 101)
        with self.assertRaisesRegex(GameError, "self_accuse"):
            game.accuse(1, 1, 101)
        with self.assertRaisesRegex(GameError, "target_missing"):
            game.accuse(1, 55, 101)
        game.accuse(1, 2, 101)
        with self.assertRaisesRegex(GameError, "active_only"):
            game.accuse(2, 1, 102)
        with self.assertRaisesRegex(GameError, "not_player"):
            game.vote(55, True, 102)
        game.vote(1, True, 102)
        with self.assertRaisesRegex(GameError, "duplicate_vote"):
            game.vote(1, False, 103)
        with self.assertRaisesRegex(GameError, "stale"):
            game.vote(2, True, 131)

    def test_strict_majority_not_majority_of_votes_cast(self):
        game = active_game(count=4)
        accuser = next(uid for uid in game.players if uid != game.spy_id)
        game.accuse(accuser, game.spy_id, 101)
        game.vote(1, True, 102)
        game.vote(2, True, 102)
        game.resolve_vote(131)
        self.assertEqual(game.winner, "spy")
        self.assertEqual(game.reason, "rejected_reason")

    def test_wrong_accused_spy_wins(self):
        game = active_game()
        accused = next(uid for uid in game.players if uid != game.spy_id)
        accuser = next(uid for uid in game.players if uid != accused)
        game.accuse(accuser, accused, 101)
        for uid in game.players:
            game.vote(uid, True, 102)
        game.resolve_vote(102)
        self.assertEqual(game.reason, "wrong_person_reason")

    def guessing_game(self):
        game = active_game()
        accuser = next(uid for uid in game.players if uid != game.spy_id)
        game.accuse(accuser, game.spy_id, 101)
        for uid in game.players:
            game.vote(uid, True, 102)
        game.resolve_vote(102)
        self.assertEqual(game.phase, Phase.GUESS)
        return game

    def test_last_chance_correct_wrong_unauthorized_and_once(self):
        game = self.guessing_game()
        index = game.locations.index(game.location)
        other = next(uid for uid in game.players if uid != game.spy_id)
        with self.assertRaisesRegex(GameError, "stale"):
            game.guess(other, index, 103)
        game.guess(game.spy_id, index, 103)
        self.assertEqual(game.winner, "spy")
        with self.assertRaisesRegex(GameError, "stale"):
            game.guess(game.spy_id, index, 104)
        game = self.guessing_game()
        wrong = (game.locations.index(game.location) + 1) % len(game.locations)
        game.guess(game.spy_id, wrong, 103)
        self.assertEqual(game.winner, "civilians")

    def test_deadline_and_limited_vote_window(self):
        game = active_game()
        seconds = game.accuse(1, 2, game.deadline - 5)
        self.assertEqual(seconds, 5)
        self.assertEqual(game.vote_deadline, game.deadline)
        game = self.guessing_game()
        with self.assertRaisesRegex(GameError, "stale"):
            game.guess(game.spy_id, 0, game.guess_deadline)

    def test_storage_group_isolation_and_idempotent_stats(self):
        store = MemoryStorage()
        one, two = active_game(-1), active_game(-2)
        store.save(one)
        store.save(two)
        one.finish("civilians", "wrong_guess_reason")
        store.record(one)
        store.record(one)
        store.delete(-1, "outdated")
        self.assertIs(store.get(-1), one)
        store.delete(-1, one.sid)
        self.assertIs(store.get(-2), two)
        self.assertEqual(sum(s.games for s in store.stats(-1)), 3)
        self.assertEqual(sum(s.spy for s in store.stats(-1)), 1)
        self.assertEqual(sum(s.wins for s in store.stats(-1)), 2)
        self.assertEqual(store.stats(-2), [])

    def test_russian_language_game_and_switching(self):
        from locations import LOCATIONS_RU
        game = Game(-100, "Тестовая группа", 1, lang="ru")
        self.assertEqual(game.lang, "ru")
        for uid in range(1, 4):
            game.join(Player(uid, f"Игрок {uid}"))
        game.deal(1, random.Random(42))
        self.assertIn(game.location, LOCATIONS_RU)
        self.assertTrue(all(role in LOCATIONS_RU[game.location] for role in game.roles.values()))

        # Switch language back to uz
        game.phase = Phase.LOBBY
        game.set_language("uz")
        self.assertEqual(game.lang, "uz")
        game.deal(1, random.Random(42))
        self.assertIn(game.location, LOCATIONS)

    def test_storage_language_preferences(self):
        store = MemoryStorage()
        self.assertEqual(store.get_chat_lang(-100), "uz")
        store.set_chat_lang(-100, "ru")
        self.assertEqual(store.get_chat_lang(-100), "ru")

        self.assertEqual(store.get_user_lang(12345), "uz")
        store.set_user_lang(12345, "ru")
        self.assertEqual(store.get_user_lang(12345), "ru")
        store.set_user_lang(12345, "uz")
        self.assertEqual(store.get_user_lang(12345), "uz")
