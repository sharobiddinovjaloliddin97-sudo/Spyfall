"""Storage boundary; replace MemoryStorage to add SQLite persistence."""

import asyncio
from collections import defaultdict
from dataclasses import dataclass
from typing import Protocol

from game import Game


@dataclass
class Stat:
    name: str
    games: int = 0
    spy: int = 0
    wins: int = 0


class Storage(Protocol):
    def get(self, chat_id: int) -> Game | None: ...
    def save(self, game: Game) -> None: ...
    def delete(self, chat_id: int, sid: str) -> None: ...
    def record(self, game: Game) -> None: ...
    def stats(self, chat_id: int) -> list[Stat]: ...
    def get_chat_lang(self, chat_id: int) -> str: ...
    def set_chat_lang(self, chat_id: int, lang: str) -> None: ...
    def get_user_lang(self, user_id: int) -> str: ...
    def set_user_lang(self, user_id: int, lang: str) -> None: ...


class MemoryStorage:
    def __init__(self):
        self._games = {}
        self._stats = defaultdict(dict)
        self._recorded = set()
        self._chat_langs = {}
        self._user_langs = {}

    def get(self, chat_id):
        return self._games.get(chat_id)

    def save(self, game):
        self._games[game.chat_id] = game

    def delete(self, chat_id, sid):
        current = self.get(chat_id)
        if current and current.sid == sid:
            del self._games[chat_id]

    def record(self, game):
        key = (game.chat_id, game.sid)
        if key in self._recorded or game.winner is None:
            return
        self._recorded.add(key)
        for uid, player in game.players.items():
            stat = self._stats[game.chat_id].setdefault(uid, Stat(player.name))
            stat.name = player.name
            stat.games += 1
            stat.spy += uid == game.spy_id
            stat.wins += (game.winner == "spy" and uid == game.spy_id) or (
                game.winner == "civilians" and uid != game.spy_id
            )

    def stats(self, chat_id):
        return sorted(
            self._stats.get(chat_id, {}).values(),
            key=lambda stat: (-stat.wins, stat.name),
        )

    def get_chat_lang(self, chat_id):
        return self._chat_langs.get(chat_id, "uz")

    def set_chat_lang(self, chat_id, lang):
        self._chat_langs[chat_id] = lang

    def get_user_lang(self, user_id):
        return self._user_langs.get(user_id, "uz")

    def set_user_lang(self, user_id, lang):
        self._user_langs[user_id] = lang



class ChatLocks:
    """Runtime locks stay outside stored game models for future persistence."""

    def __init__(self):
        self._locks = defaultdict(asyncio.Lock)

    def for_chat(self, chat_id):
        return self._locks[chat_id]
