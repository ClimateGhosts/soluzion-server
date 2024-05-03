import enum
import inspect
from dataclasses import dataclass
from typing import Optional

import soluzion_server.soluzion_types
from soluzion_server.soluzion_expanded import Problem, ExpandedState

PROBLEM: Problem | None = None


# region Global Data Structures


@dataclass
class PlayerSession:
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


connected_players: dict[str, PlayerSession] = {}

room_sessions: dict[str, RoomSession] = {}


# endregion

# region Global Functions


def current_player(sid: str) -> PlayerSession | None:
    if sid in connected_players:
        return connected_players[sid]
    return None


def current_room(sid: str) -> RoomSession | None:
    player = current_player(sid)
    if player is None or player.room not in room_sessions:
        return None
    return room_sessions[player.room]


def current_game(sid: str) -> GameSession | None:
    room = current_room(sid)
    if room is None:
        return None

    return room.game


# end region


# region Misc

# Default Python enum stringify is not helpful for this project, would prefer it to just be the value

for name, obj in inspect.getmembers(soluzion_server.soluzion_types):
    if inspect.isclass(obj) and issubclass(obj, enum.Enum):

        def new_str(self):
            return str(self.value)

        obj.__str__ = new_str

# end region
