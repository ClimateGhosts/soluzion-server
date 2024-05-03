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


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


class SharedEvent(Enum):
    """Primary copy of Soluzion Types; used to generate others for Python, C# etc."""

    CONNECT = "connect"
    DISCONNECT = "disconnect"


class CreateRoom:
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
    role: Optional[float]
    room: str
    username: str

    def __init__(self, role: Optional[float], room: str, username: str) -> None:
        self.role = role
        self.room = room
        self.username = username

    @staticmethod
    def from_dict(obj: Any) -> 'JoinRoom':
        assert isinstance(obj, dict)
        role = from_union([from_none, from_float], obj.get("role"))
        room = from_str(obj.get("room"))
        username = from_str(obj.get("username"))
        return JoinRoom(role, room, username)

    def to_dict(self) -> dict:
        result: dict = {}
        result["role"] = from_union([from_none, to_float], self.role)
        result["room"] = from_str(self.room)
        result["username"] = from_str(self.username)
        return result


class OperatorChosen:
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


class ServerEvents:
    """Events handled by the server (sent by the client)"""

    create_room: CreateRoom
    join_room: JoinRoom
    operator_chosen: OperatorChosen

    def __init__(self, create_room: CreateRoom, join_room: JoinRoom, operator_chosen: OperatorChosen) -> None:
        self.create_room = create_room
        self.join_room = join_room
        self.operator_chosen = operator_chosen

    @staticmethod
    def from_dict(obj: Any) -> 'ServerEvents':
        assert isinstance(obj, dict)
        create_room = CreateRoom.from_dict(obj.get("create_room"))
        join_room = JoinRoom.from_dict(obj.get("join_room"))
        operator_chosen = OperatorChosen.from_dict(obj.get("operator_chosen"))
        return ServerEvents(create_room, join_room, operator_chosen)

    def to_dict(self) -> dict:
        result: dict = {}
        result["create_room"] = to_class(CreateRoom, self.create_room)
        result["join_room"] = to_class(JoinRoom, self.join_room)
        result["operator_chosen"] = to_class(OperatorChosen, self.operator_chosen)
        return result


class ServerError(Enum):
    CANT_JOIN_ROOM = "CantJoinRoom"
    GAME_ALREADY_STARTED = "GameAlreadyStarted"
    GAME_NOT_STARTED = "GameNotStarted"
    INVALID_OPERATOR = "InvalidOperator"
    NOT_IN_A_ROOM = "NotInARoom"
    ROOM_ALREADY_EXISTS = "RoomAlreadyExists"


class ServerEvent(Enum):
    CREATE_ROOM = "create_room"
    JOIN_ROOM = "join_room"
    LEAVE_ROOM = "leave_room"
    OPERATOR_CHOSEN = "operator_chosen"
    START_GAME = "start_game"


class Error:
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


class Operator:
    name: str
    op_no: float
    params: Optional[List[Param]]

    def __init__(self, name: str, op_no: float, params: Optional[List[Param]]) -> None:
        self.name = name
        self.op_no = op_no
        self.params = params

    @staticmethod
    def from_dict(obj: Any) -> 'Operator':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        op_no = from_float(obj.get("op_no"))
        params = from_union([lambda x: from_list(Param.from_dict, x), from_none], obj.get("params"))
        return Operator(name, op_no, params)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["op_no"] = to_float(self.op_no)
        result["params"] = from_union([lambda x: from_list(lambda x: to_class(Param, x), x), from_none], self.params)
        return result


class OperatorsAvailable:
    operators: List[Operator]

    def __init__(self, operators: List[Operator]) -> None:
        self.operators = operators

    @staticmethod
    def from_dict(obj: Any) -> 'OperatorsAvailable':
        assert isinstance(obj, dict)
        operators = from_list(Operator.from_dict, obj.get("operators"))
        return OperatorsAvailable(operators)

    def to_dict(self) -> dict:
        result: dict = {}
        result["operators"] = from_list(lambda x: to_class(Operator, x), self.operators)
        return result


class RoomCreated:
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


class StateUpdated:
    message: str
    state: Optional[Dict[str, Any]]

    def __init__(self, message: str, state: Optional[Dict[str, Any]]) -> None:
        self.message = message
        self.state = state

    @staticmethod
    def from_dict(obj: Any) -> 'StateUpdated':
        assert isinstance(obj, dict)
        message = from_str(obj.get("message"))
        state = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("state"))
        return StateUpdated(message, state)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message"] = from_str(self.message)
        result["state"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.state)
        return result


class ClientEvents:
    """Events handled by the client (sent by the server)"""

    error: Error
    operators_available: OperatorsAvailable
    room_created: RoomCreated
    room_joined: RoomJoined
    room_left: RoomLeft
    state_updated: StateUpdated

    def __init__(self, error: Error, operators_available: OperatorsAvailable, room_created: RoomCreated, room_joined: RoomJoined, room_left: RoomLeft, state_updated: StateUpdated) -> None:
        self.error = error
        self.operators_available = operators_available
        self.room_created = room_created
        self.room_joined = room_joined
        self.room_left = room_left
        self.state_updated = state_updated

    @staticmethod
    def from_dict(obj: Any) -> 'ClientEvents':
        assert isinstance(obj, dict)
        error = Error.from_dict(obj.get("error"))
        operators_available = OperatorsAvailable.from_dict(obj.get("operators_available"))
        room_created = RoomCreated.from_dict(obj.get("room_created"))
        room_joined = RoomJoined.from_dict(obj.get("room_joined"))
        room_left = RoomLeft.from_dict(obj.get("room_left"))
        state_updated = StateUpdated.from_dict(obj.get("state_updated"))
        return ClientEvents(error, operators_available, room_created, room_joined, room_left, state_updated)

    def to_dict(self) -> dict:
        result: dict = {}
        result["error"] = to_class(Error, self.error)
        result["operators_available"] = to_class(OperatorsAvailable, self.operators_available)
        result["room_created"] = to_class(RoomCreated, self.room_created)
        result["room_joined"] = to_class(RoomJoined, self.room_joined)
        result["room_left"] = to_class(RoomLeft, self.room_left)
        result["state_updated"] = to_class(StateUpdated, self.state_updated)
        return result


class ClientEvent(Enum):
    ERROR = "error"
    GAME_ENDED = "game_ended"
    GAME_STARTED = "game_started"
    OPERATORS_AVAILABLE = "operators_available"
    ROOM_CREATED = "room_created"
    ROOM_JOINED = "room_joined"
    ROOM_LEFT = "room_left"
    STATE_UPDATED = "state_updated"


class OperatorParam:
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
    def from_dict(obj: Any) -> 'OperatorParam':
        assert isinstance(obj, dict)
        max = from_union([from_none, from_float], obj.get("max"))
        min = from_union([from_none, from_float], obj.get("min"))
        name = from_str(obj.get("name"))
        type = TypeEnum(obj.get("type"))
        return OperatorParam(max, min, name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["max"] = from_union([from_none, to_float], self.max)
        result["min"] = from_union([from_none, to_float], self.min)
        result["name"] = from_str(self.name)
        result["type"] = to_enum(TypeEnum, self.type)
        return result


def shared_event_from_dict(s: Any) -> SharedEvent:
    return SharedEvent(s)


def shared_event_to_dict(x: SharedEvent) -> Any:
    return to_enum(SharedEvent, x)


def server_error_from_dict(s: Any) -> ServerError:
    return ServerError(s)


def server_error_to_dict(x: ServerError) -> Any:
    return to_enum(ServerError, x)


def server_events_from_dict(s: Any) -> ServerEvents:
    return ServerEvents.from_dict(s)


def server_events_to_dict(x: ServerEvents) -> Any:
    return to_class(ServerEvents, x)


def server_event_from_dict(s: Any) -> ServerEvent:
    return ServerEvent(s)


def server_event_to_dict(x: ServerEvent) -> Any:
    return to_enum(ServerEvent, x)


def client_events_from_dict(s: Any) -> ClientEvents:
    return ClientEvents.from_dict(s)


def client_events_to_dict(x: ClientEvents) -> Any:
    return to_class(ClientEvents, x)


def client_event_from_dict(s: Any) -> ClientEvent:
    return ClientEvent(s)


def client_event_to_dict(x: ClientEvent) -> Any:
    return to_enum(ClientEvent, x)


def operator_param_from_dict(s: Any) -> OperatorParam:
    return OperatorParam.from_dict(s)


def operator_param_to_dict(x: OperatorParam) -> Any:
    return to_class(OperatorParam, x)
