from enum import Enum
from typing import Any, Optional, List, Dict, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class SharedEvent(Enum):
    """Events handled and sent by both client and server"""

    CONNECT = "connect"
    DISCONNECT = "disconnect"


class CreateRoom:
    """Request for the server to create a new room"""

    room: str

    def __init__(self, room: str) -> None:
        self.room = room

    @staticmethod
    def from_dict(obj: Any) -> 'CreateRoom':
        assert isinstance(obj, dict)
        room = from_str(obj.get("room"))
        return CreateRoom(room)

    def to_dict(self) -> dict:
        result: dict = {}
        result["room"] = from_str(self.room)
        return result


class JoinRoom:
    """Request for the sender to join an existing room, optionally setting a username"""

    room: str
    username: Optional[str]

    def __init__(self, room: str, username: Optional[str]) -> None:
        self.room = room
        self.username = username

    @staticmethod
    def from_dict(obj: Any) -> 'JoinRoom':
        assert isinstance(obj, dict)
        room = from_str(obj.get("room"))
        username = from_union([from_none, from_str], obj.get("username"))
        return JoinRoom(room, username)

    def to_dict(self) -> dict:
        result: dict = {}
        result["room"] = from_str(self.room)
        result["username"] = from_union([from_none, from_str], self.username)
        return result


class OperatorChosen:
    """Request for a specific operator to be replied within the sender's game session"""

    op_no: float
    params: Optional[List[Any]]

    def __init__(self, op_no: float, params: Optional[List[Any]]) -> None:
        self.op_no = op_no
        self.params = params

    @staticmethod
    def from_dict(obj: Any) -> 'OperatorChosen':
        assert isinstance(obj, dict)
        op_no = from_float(obj.get("op_no"))
        params = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("params"))
        return OperatorChosen(op_no, params)

    def to_dict(self) -> dict:
        result: dict = {}
        result["op_no"] = to_float(self.op_no)
        result["params"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.params)
        return result


class SetName:
    """Request to set the sender's username"""

    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'SetName':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        return SetName(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        return result


class SetRoles:
    """Request to set the sender's roles"""

    roles: List[float]

    def __init__(self, roles: List[float]) -> None:
        self.roles = roles

    @staticmethod
    def from_dict(obj: Any) -> 'SetRoles':
        assert isinstance(obj, dict)
        roles = from_list(from_float, obj.get("roles"))
        return SetRoles(roles)

    def to_dict(self) -> dict:
        result: dict = {}
        result["roles"] = from_list(to_float, self.roles)
        return result


class ServerEvents:
    create_room: CreateRoom
    """Request for the server to create a new room"""

    join_room: JoinRoom
    """Request for the sender to join an existing room, optionally setting a username"""

    leave_room: Dict[str, Any]
    """Request for the sender to leave their current room"""

    operator_chosen: OperatorChosen
    """Request for a specific operator to be replied within the sender's game session"""

    set_name: SetName
    """Request to set the sender's username"""

    set_roles: SetRoles
    """Request to set the sender's roles"""

    start_game: Dict[str, Any]
    """Request to start the game for the sender's current room"""

    def __init__(self, create_room: CreateRoom, join_room: JoinRoom, leave_room: Dict[str, Any], operator_chosen: OperatorChosen, set_name: SetName, set_roles: SetRoles, start_game: Dict[str, Any]) -> None:
        self.create_room = create_room
        self.join_room = join_room
        self.leave_room = leave_room
        self.operator_chosen = operator_chosen
        self.set_name = set_name
        self.set_roles = set_roles
        self.start_game = start_game

    @staticmethod
    def from_dict(obj: Any) -> 'ServerEvents':
        assert isinstance(obj, dict)
        create_room = CreateRoom.from_dict(obj.get("create_room"))
        join_room = JoinRoom.from_dict(obj.get("join_room"))
        leave_room = from_dict(lambda x: x, obj.get("leave_room"))
        operator_chosen = OperatorChosen.from_dict(obj.get("operator_chosen"))
        set_name = SetName.from_dict(obj.get("set_name"))
        set_roles = SetRoles.from_dict(obj.get("set_roles"))
        start_game = from_dict(lambda x: x, obj.get("start_game"))
        return ServerEvents(create_room, join_room, leave_room, operator_chosen, set_name, set_roles, start_game)

    def to_dict(self) -> dict:
        result: dict = {}
        result["create_room"] = to_class(CreateRoom, self.create_room)
        result["join_room"] = to_class(JoinRoom, self.join_room)
        result["leave_room"] = from_dict(lambda x: x, self.leave_room)
        result["operator_chosen"] = to_class(OperatorChosen, self.operator_chosen)
        result["set_name"] = to_class(SetName, self.set_name)
        result["set_roles"] = to_class(SetRoles, self.set_roles)
        result["start_game"] = from_dict(lambda x: x, self.start_game)
        return result


class ClientEvent(Enum):
    ERROR = "error"
    GAME_ENDED = "game_ended"
    GAME_STARTED = "game_started"
    OPERATORS_AVAILABLE = "operators_available"
    OPERATOR_APPLIED = "operator_applied"
    ROLES_CHANGED = "roles_changed"
    ROOM_CREATED = "room_created"
    ROOM_JOINED = "room_joined"
    ROOM_LEFT = "room_left"
    TRANSITION = "transition"


class ServerError(Enum):
    CANT_JOIN_ROOM = "CantJoinRoom"
    GAME_ALREADY_STARTED = "GameAlreadyStarted"
    GAME_NOT_STARTED = "GameNotStarted"
    INVALID_OPERATOR = "InvalidOperator"
    INVALID_ROLES = "InvalidRoles"
    NOT_IN_A_ROOM = "NotInARoom"
    ROOM_ALREADY_EXISTS = "RoomAlreadyExists"


class ServerEvent(Enum):
    """Events handled by the server (sent by the client)"""

    CREATE_ROOM = "create_room"
    JOIN_ROOM = "join_room"
    LEAVE_ROOM = "leave_room"
    OPERATOR_CHOSEN = "operator_chosen"
    SET_NAME = "set_name"
    SET_ROLES = "set_roles"
    START_GAME = "start_game"


class Error:
    """An error has been caused by one of the ServerEvents this client has sent"""

    error: ServerError
    event: ServerEvent
    message: Optional[str]

    def __init__(self, error: ServerError, event: ServerEvent, message: Optional[str]) -> None:
        self.error = error
        self.event = event
        self.message = message

    @staticmethod
    def from_dict(obj: Any) -> 'Error':
        assert isinstance(obj, dict)
        error = ServerError(obj.get("error"))
        event = ServerEvent(obj.get("event"))
        message = from_union([from_none, from_str], obj.get("message"))
        return Error(error, event, message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["error"] = to_enum(ServerError, self.error)
        result["event"] = to_enum(ServerEvent, self.event)
        result["message"] = from_union([from_none, from_str], self.message)
        return result


class GameEnded:
    """The game has ended for the current client's room"""

    message: str

    def __init__(self, message: str) -> None:
        self.message = message

    @staticmethod
    def from_dict(obj: Any) -> 'GameEnded':
        assert isinstance(obj, dict)
        message = from_str(obj.get("message"))
        return GameEnded(message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message"] = from_str(self.message)
        return result


class GameStarted:
    """The game has been started for the current client's room"""

    message: str
    """new state's __str__ message"""

    state: Optional[str]
    """JSON representation of new state"""

    def __init__(self, message: str, state: Optional[str]) -> None:
        self.message = message
        self.state = state

    @staticmethod
    def from_dict(obj: Any) -> 'GameStarted':
        assert isinstance(obj, dict)
        message = from_str(obj.get("message"))
        state = from_union([from_none, from_str], obj.get("state"))
        return GameStarted(message, state)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message"] = from_str(self.message)
        result["state"] = from_union([from_none, from_str], self.state)
        return result


class OperatorAppliedOperator:
    name: str
    op_no: float
    params: Optional[List[Any]]

    def __init__(self, name: str, op_no: float, params: Optional[List[Any]]) -> None:
        self.name = name
        self.op_no = op_no
        self.params = params

    @staticmethod
    def from_dict(obj: Any) -> 'OperatorAppliedOperator':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        op_no = from_float(obj.get("op_no"))
        params = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("params"))
        return OperatorAppliedOperator(name, op_no, params)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["op_no"] = to_float(self.op_no)
        result["params"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.params)
        return result


class OperatorApplied:
    """An operator was applied for the current client's game, transforming the state"""

    message: str
    """new state's __str__ output"""

    operator: OperatorAppliedOperator
    state: Optional[str]
    """JSON representation of new state"""

    def __init__(self, message: str, operator: OperatorAppliedOperator, state: Optional[str]) -> None:
        self.message = message
        self.operator = operator
        self.state = state

    @staticmethod
    def from_dict(obj: Any) -> 'OperatorApplied':
        assert isinstance(obj, dict)
        message = from_str(obj.get("message"))
        operator = OperatorAppliedOperator.from_dict(obj.get("operator"))
        state = from_union([from_none, from_str], obj.get("state"))
        return OperatorApplied(message, operator, state)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message"] = from_str(self.message)
        result["operator"] = to_class(OperatorAppliedOperator, self.operator)
        result["state"] = from_union([from_none, from_str], self.state)
        return result


class TypeEnum(Enum):
    FLOAT = "float"
    INT = "int"
    STR = "str"


class Param:
    max: Optional[float]
    min: Optional[float]
    name: str
    type: TypeEnum

    def __init__(self, max: Optional[float], min: Optional[float], name: str, type: TypeEnum) -> None:
        self.max = max
        self.min = min
        self.name = name
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Param':
        assert isinstance(obj, dict)
        max = from_union([from_none, from_float], obj.get("max"))
        min = from_union([from_none, from_float], obj.get("min"))
        name = from_str(obj.get("name"))
        type = TypeEnum(obj.get("type"))
        return Param(max, min, name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["max"] = from_union([from_none, to_float], self.max)
        result["min"] = from_union([from_none, to_float], self.min)
        result["name"] = from_str(self.name)
        result["type"] = to_enum(TypeEnum, self.type)
        return result


class OperatorElement:
    name: str
    op_no: float
    params: Optional[List[Param]]

    def __init__(self, name: str, op_no: float, params: Optional[List[Param]]) -> None:
        self.name = name
        self.op_no = op_no
        self.params = params

    @staticmethod
    def from_dict(obj: Any) -> 'OperatorElement':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        op_no = from_float(obj.get("op_no"))
        params = from_union([lambda x: from_list(Param.from_dict, x), from_none], obj.get("params"))
        return OperatorElement(name, op_no, params)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["op_no"] = to_float(self.op_no)
        result["params"] = from_union([lambda x: from_list(lambda x: to_class(Param, x), x), from_none], self.params)
        return result


class OperatorsAvailable:
    """A new set of operators is available for the current client"""

    operators: List[OperatorElement]

    def __init__(self, operators: List[OperatorElement]) -> None:
        self.operators = operators

    @staticmethod
    def from_dict(obj: Any) -> 'OperatorsAvailable':
        assert isinstance(obj, dict)
        operators = from_list(OperatorElement.from_dict, obj.get("operators"))
        return OperatorsAvailable(operators)

    def to_dict(self) -> dict:
        result: dict = {}
        result["operators"] = from_list(lambda x: to_class(OperatorElement, x), self.operators)
        return result


class RolesChanged:
    """A user in the current room has a changed set of roles"""

    roles: List[float]
    """Role numbers are indices within the Soluzion problem's ROLES array"""

    username: str

    def __init__(self, roles: List[float], username: str) -> None:
        self.roles = roles
        self.username = username

    @staticmethod
    def from_dict(obj: Any) -> 'RolesChanged':
        assert isinstance(obj, dict)
        roles = from_list(from_float, obj.get("roles"))
        username = from_str(obj.get("username"))
        return RolesChanged(roles, username)

    def to_dict(self) -> dict:
        result: dict = {}
        result["roles"] = from_list(to_float, self.roles)
        result["username"] = from_str(self.username)
        return result


class RoomCreated:
    """A room/lobby with the given name has been created"""

    room: str

    def __init__(self, room: str) -> None:
        self.room = room

    @staticmethod
    def from_dict(obj: Any) -> 'RoomCreated':
        assert isinstance(obj, dict)
        room = from_str(obj.get("room"))
        return RoomCreated(room)

    def to_dict(self) -> dict:
        result: dict = {}
        result["room"] = from_str(self.room)
        return result


class RoomJoined:
    """A user has joined the client's room"""

    username: str

    def __init__(self, username: str) -> None:
        self.username = username

    @staticmethod
    def from_dict(obj: Any) -> 'RoomJoined':
        assert isinstance(obj, dict)
        username = from_str(obj.get("username"))
        return RoomJoined(username)

    def to_dict(self) -> dict:
        result: dict = {}
        result["username"] = from_str(self.username)
        return result


class RoomLeft:
    """A user has left the current client's room"""

    username: str

    def __init__(self, username: str) -> None:
        self.username = username

    @staticmethod
    def from_dict(obj: Any) -> 'RoomLeft':
        assert isinstance(obj, dict)
        username = from_str(obj.get("username"))
        return RoomLeft(username)

    def to_dict(self) -> dict:
        result: dict = {}
        result["username"] = from_str(self.username)
        return result


class Transition:
    """A transition event has occurred for the current client's game"""

    message: str

    def __init__(self, message: str) -> None:
        self.message = message

    @staticmethod
    def from_dict(obj: Any) -> 'Transition':
        assert isinstance(obj, dict)
        message = from_str(obj.get("message"))
        return Transition(message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message"] = from_str(self.message)
        return result


class ClientEvents:
    error: Error
    """An error has been caused by one of the ServerEvents this client has sent"""

    game_ended: GameEnded
    """The game has ended for the current client's room"""

    game_started: GameStarted
    """The game has been started for the current client's room"""

    operator_applied: OperatorApplied
    """An operator was applied for the current client's game, transforming the state"""

    operators_available: OperatorsAvailable
    """A new set of operators is available for the current client"""

    roles_changed: RolesChanged
    """A user in the current room has a changed set of roles"""

    room_created: RoomCreated
    """A room/lobby with the given name has been created"""

    room_joined: RoomJoined
    """A user has joined the client's room"""

    room_left: RoomLeft
    """A user has left the current client's room"""

    transition: Transition
    """A transition event has occurred for the current client's game"""

    def __init__(self, error: Error, game_ended: GameEnded, game_started: GameStarted, operator_applied: OperatorApplied, operators_available: OperatorsAvailable, roles_changed: RolesChanged, room_created: RoomCreated, room_joined: RoomJoined, room_left: RoomLeft, transition: Transition) -> None:
        self.error = error
        self.game_ended = game_ended
        self.game_started = game_started
        self.operator_applied = operator_applied
        self.operators_available = operators_available
        self.roles_changed = roles_changed
        self.room_created = room_created
        self.room_joined = room_joined
        self.room_left = room_left
        self.transition = transition

    @staticmethod
    def from_dict(obj: Any) -> 'ClientEvents':
        assert isinstance(obj, dict)
        error = Error.from_dict(obj.get("error"))
        game_ended = GameEnded.from_dict(obj.get("game_ended"))
        game_started = GameStarted.from_dict(obj.get("game_started"))
        operator_applied = OperatorApplied.from_dict(obj.get("operator_applied"))
        operators_available = OperatorsAvailable.from_dict(obj.get("operators_available"))
        roles_changed = RolesChanged.from_dict(obj.get("roles_changed"))
        room_created = RoomCreated.from_dict(obj.get("room_created"))
        room_joined = RoomJoined.from_dict(obj.get("room_joined"))
        room_left = RoomLeft.from_dict(obj.get("room_left"))
        transition = Transition.from_dict(obj.get("transition"))
        return ClientEvents(error, game_ended, game_started, operator_applied, operators_available, roles_changed, room_created, room_joined, room_left, transition)

    def to_dict(self) -> dict:
        result: dict = {}
        result["error"] = to_class(Error, self.error)
        result["game_ended"] = to_class(GameEnded, self.game_ended)
        result["game_started"] = to_class(GameStarted, self.game_started)
        result["operator_applied"] = to_class(OperatorApplied, self.operator_applied)
        result["operators_available"] = to_class(OperatorsAvailable, self.operators_available)
        result["roles_changed"] = to_class(RolesChanged, self.roles_changed)
        result["room_created"] = to_class(RoomCreated, self.room_created)
        result["room_joined"] = to_class(RoomJoined, self.room_joined)
        result["room_left"] = to_class(RoomLeft, self.room_left)
        result["transition"] = to_class(Transition, self.transition)
        return result


class Role:
    max: Optional[float]
    min: Optional[float]
    name: str

    def __init__(self, max: Optional[float], min: Optional[float], name: str) -> None:
        self.max = max
        self.min = min
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Role':
        assert isinstance(obj, dict)
        max = from_union([from_none, from_float], obj.get("max"))
        min = from_union([from_none, from_float], obj.get("min"))
        name = from_str(obj.get("name"))
        return Role(max, min, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["max"] = from_union([from_none, to_float], self.max)
        result["min"] = from_union([from_none, to_float], self.min)
        result["name"] = from_str(self.name)
        return result


def shared_event_from_dict(s: Any) -> SharedEvent:
    return SharedEvent(s)


def shared_event_to_dict(x: SharedEvent) -> Any:
    return to_enum(SharedEvent, x)


def server_event_from_dict(s: Any) -> ServerEvent:
    return ServerEvent(s)


def server_event_to_dict(x: ServerEvent) -> Any:
    return to_enum(ServerEvent, x)


def server_events_from_dict(s: Any) -> ServerEvents:
    return ServerEvents.from_dict(s)


def server_events_to_dict(x: ServerEvents) -> Any:
    return to_class(ServerEvents, x)


def client_event_from_dict(s: Any) -> ClientEvent:
    return ClientEvent(s)


def client_event_to_dict(x: ClientEvent) -> Any:
    return to_enum(ClientEvent, x)


def client_events_from_dict(s: Any) -> ClientEvents:
    return ClientEvents.from_dict(s)


def client_events_to_dict(x: ClientEvents) -> Any:
    return to_class(ClientEvents, x)


def server_error_from_dict(s: Any) -> ServerError:
    return ServerError(s)


def server_error_to_dict(x: ServerError) -> Any:
    return to_enum(ServerError, x)


def role_from_dict(s: Any) -> Role:
    return Role.from_dict(s)


def role_to_dict(x: Role) -> Any:
    return to_class(Role, x)
