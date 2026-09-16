"""Pure game state and rules, independent of Telegram and storage."""

import math
import secrets
from dataclasses import dataclass, field
from enum import Enum

from locations import LOCATIONS, get_locations


class Phase(str, Enum):
    LOBBY = "lobby"
    DEALING = "dealing"
    ACTIVE = "active"
    VOTING = "voting"
    GUESS = "guess"
    ENDED = "ended"


class GameError(Exception):
    """Exception carries a texts.py key, not a Telegram-specific response."""


@dataclass
class Player:
    id: int
    name: str
    username: str | None = None


@dataclass
class Game:
    chat_id: int
    title: str
    owner_id: int
    sid: str = field(default_factory=lambda: secrets.token_hex(4))
    phase: Phase = Phase.LOBBY
    minutes: int = 8
    lang: str = "uz"
    players: dict[int, Player] = field(default_factory=dict)
    location: str | None = None
    spy_id: int | None = None
    first_player_id: int | None = None
    lobby_message_id: int | None = None
    roles: dict[int, str] = field(default_factory=dict)
    locations: tuple[str, ...] = field(
        default_factory=lambda: tuple(LOCATIONS)
    )
    deadline: float = 0
    vote_deadline: float = 0
    guess_deadline: float = 0
    accused: int | None = None
    votes: dict[int, bool] = field(default_factory=dict)
    winner: str | None = None
    reason: str | None = None

    def require(self, phase, key="stale"):
        if self.phase != phase:
            raise GameError(key)

    def require_player(self, user_id):
        if user_id not in self.players:
            raise GameError("not_player")

    def set_language(self, lang: str):
        self.require(Phase.LOBBY, "lobby_only")
        self.lang = lang
        self.locations = tuple(get_locations(lang))

    def join(self, player):
        self.require(Phase.LOBBY, "lobby_only")
        if player.id in self.players:
            raise GameError("already_joined")
        if len(self.players) >= 10:
            raise GameError("full")
        self.players[player.id] = player

    def leave(self, user_id):
        self.require(Phase.LOBBY, "lobby_only")
        self.require_player(user_id)
        del self.players[user_id]

    def deal(self, user_id, rng=None):
        self.require(Phase.LOBBY, "lobby_only")
        self.require_player(user_id)
        if len(self.players) < 3:
            raise GameError("minimum")
        rng = rng or secrets.SystemRandom()
        loc_dict = get_locations(self.lang)
        self.locations = tuple(loc_dict)
        self.location = rng.choice(self.locations)
        self.spy_id = rng.choice(tuple(self.players))
        self.first_player_id = rng.choice(tuple(self.players))
        self.roles = {
            uid: rng.choice(loc_dict[self.location])
            for uid in self.players
            if uid != self.spy_id
        }
        self.phase = Phase.DEALING


    def reset_lobby(self):
        self.phase = Phase.LOBBY
        self.location = None
        self.spy_id = None
        self.first_player_id = None
        self.roles = {}

    def activate(self, now):
        self.require(Phase.DEALING)
        self.deadline = now + self.minutes * 60
        self.phase = Phase.ACTIVE

    def accuse(self, accuser, accused, now):
        self.require(Phase.ACTIVE, "active_only")
        self.require_player(accuser)
        if accused not in self.players:
            raise GameError("target_missing")
        if accuser == accused:
            raise GameError("self_accuse")
        if now >= self.deadline:
            raise GameError("stale")
        self.accused = accused
        self.votes = {}
        self.vote_deadline = min(now + 30, self.deadline)
        self.phase = Phase.VOTING
        return max(1, math.ceil(self.vote_deadline - now))

    def vote(self, user_id, value, now):
        self.require(Phase.VOTING)
        self.require_player(user_id)
        if now >= self.vote_deadline:
            raise GameError("stale")
        if user_id in self.votes:
            raise GameError("duplicate_vote")
        self.votes[user_id] = value
        return len(self.votes) == len(self.players)

    def resolve_vote(self, now):
        self.require(Phase.VOTING)
        if sum(self.votes.values()) <= len(self.players) // 2:
            self.finish("spy", "rejected_reason")
        elif self.accused != self.spy_id:
            self.finish("spy", "wrong_person_reason")
        else:
            self.phase = Phase.GUESS
            self.guess_deadline = now + 30

    def guess(self, user_id, index, now):
        self.require(Phase.GUESS)
        if user_id != self.spy_id or now >= self.guess_deadline:
            raise GameError("stale")
        if not 0 <= index < len(self.locations):
            raise GameError("stale")
        correct = self.locations[index] == self.location
        self.finish(
            "spy" if correct else "civilians",
            "correct_guess_reason" if correct else "wrong_guess_reason",
        )

    def finish(self, winner, reason):
        if self.phase == Phase.ENDED:
            raise GameError("stale")
        self.winner, self.reason = winner, reason
        self.phase = Phase.ENDED
