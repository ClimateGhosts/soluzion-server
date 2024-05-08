from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from soluzion_server.soluzion_expanded import Problem, ExpandedState
from soluzion_server.soluzion_types import ErrorResponse, Error, Room, RoomPlayerClass
from soluzion_server.soluzion_types import ServerError

PROBLEM: Problem | None = None


# region Global Data Structures


@dataclass
class PlayerSession:
    """Current Player Connection"""

    sid: str
    name: Optional[str]
    room: Optional[str]
    roles: set[int]


@dataclass
class GameSession:
    current_state: ExpandedState
    state_stack: list[ExpandedState]
    owner_sid: str
    room: str
    players: dict[str, set[int]]  # Mapping of sid to role number
    step: int = 0
    depth: int = 0


@dataclass
class RoomSession:
    id: str
    owner_sid: str
    player_sids: list[str]
    game: Optional[GameSession]

    def to_dict(self):
        return Room(
            self.game is not None,
            self.owner_sid,
            [
                RoomPlayerClass(
                    player.name or player.sid, list(player.roles), player.sid
                )
                for player in connected_players.values()
                if player.sid in self.player_sids
            ],
            self.id,
        ).to_dict()


connected_players: dict[str, PlayerSession] = {}

room_sessions: dict[str, RoomSession] = {}


# endregion

# region Global Functions


def current_player(sid: str) -> PlayerSession | None:
    return connected_players.get(sid)


def current_room(sid: str) -> RoomSession | None:
    player = current_player(sid)
    return None if player is None else room_sessions.get(player.room)


def current_game(sid: str) -> GameSession | None:
    room = current_room(sid)
    return None if room is None else room.game


def error_response(error: ServerError, message: str = None):
    print(error.value, message)
    return ErrorResponse(Error(message, error)).to_dict()


# end region
