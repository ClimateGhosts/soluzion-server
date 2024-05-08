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


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class SharedEvent(Enum):
    """Events handled and sent by both client and server"""

    CONNECT = "connect"
    DISCONNECT = "disconnect"


class ClientToServer(Enum):
    CREATE_ROOM = "create_room"
    DELETE_ROOM = "delete_room"
    JOIN_ROOM = "join_room"
    LEAVE_ROOM = "leave_room"
    LIST_ROLES = "list_roles"
    LIST_ROOMS = "list_rooms"
    OPERATOR_CHOSEN = "operator_chosen"
    SET_NAME = "set_name"
    SET_ROLES = "set_roles"
    START_GAME = "start_game"


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


class DeleteRoom:
    """Request for the server to delete an empty room"""

    room: str

    def __init__(self, room: str) -> None:
        self.room = room

    @staticmethod
    def from_dict(obj: Any) -> 'DeleteRoom':
        assert isinstance(obj, dict)
        room = from_str(obj.get("room"))
        return DeleteRoom(room)

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


class ClientToServerEvents:
    create_room: CreateRoom
    """Request for the server to create a new room"""

    delete_room: DeleteRoom
    """Request for the server to delete an empty room"""

    join_room: JoinRoom
    """Request for the sender to join an existing room, optionally setting a username"""

    leave_room: Dict[str, Any]
    """Request for the sender to leave their current room"""

    list_roles: Dict[str, Any]
    """Gets information about the roles of the SOLZUION Problem"""

    list_rooms: Dict[str, Any]
    """Lists all active rooms"""

    operator_chosen: OperatorChosen
    """Request for a specific operator to be replied within the sender's game session"""

    set_name: SetName
    """Request to set the sender's username"""

    set_roles: SetRoles
    """Request to set the sender's roles"""

    start_game: Dict[str, Any]
    """Request to start the game for the sender's current room"""

    def __init__(self, create_room: CreateRoom, delete_room: DeleteRoom, join_room: JoinRoom, leave_room: Dict[str, Any], list_roles: Dict[str, Any], list_rooms: Dict[str, Any], operator_chosen: OperatorChosen, set_name: SetName, set_roles: SetRoles, start_game: Dict[str, Any]) -> None:
        self.create_room = create_room
        self.delete_room = delete_room
        self.join_room = join_room
        self.leave_room = leave_room
        self.list_roles = list_roles
        self.list_rooms = list_rooms
        self.operator_chosen = operator_chosen
        self.set_name = set_name
        self.set_roles = set_roles
        self.start_game = start_game

    @staticmethod
    def from_dict(obj: Any) -> 'ClientToServerEvents':
        assert isinstance(obj, dict)
        create_room = CreateRoom.from_dict(obj.get("create_room"))
        delete_room = DeleteRoom.from_dict(obj.get("delete_room"))
        join_room = JoinRoom.from_dict(obj.get("join_room"))
        leave_room = from_dict(lambda x: x, obj.get("leave_room"))
        list_roles = from_dict(lambda x: x, obj.get("list_roles"))
        list_rooms = from_dict(lambda x: x, obj.get("list_rooms"))
        operator_chosen = OperatorChosen.from_dict(obj.get("operator_chosen"))
        set_name = SetName.from_dict(obj.get("set_name"))
        set_roles = SetRoles.from_dict(obj.get("set_roles"))
        start_game = from_dict(lambda x: x, obj.get("start_game"))
        return ClientToServerEvents(create_room, delete_room, join_room, leave_room, list_roles, list_rooms, operator_chosen, set_name, set_roles, start_game)

    def to_dict(self) -> dict:
        result: dict = {}
        result["create_room"] = to_class(CreateRoom, self.create_room)
        result["delete_room"] = to_class(DeleteRoom, self.delete_room)
        result["join_room"] = to_class(JoinRoom, self.join_room)
        result["leave_room"] = from_dict(lambda x: x, self.leave_room)
        result["list_roles"] = from_dict(lambda x: x, self.list_roles)
        result["list_rooms"] = from_dict(lambda x: x, self.list_rooms)
        result["operator_chosen"] = to_class(OperatorChosen, self.operator_chosen)
        result["set_name"] = to_class(SetName, self.set_name)
        result["set_roles"] = to_class(SetRoles, self.set_roles)
        result["start_game"] = from_dict(lambda x: x, self.start_game)
        return result


class RoleElement:
    max: Optional[float]
    min: Optional[float]
    name: str

    def __init__(self, max: Optional[float], min: Optional[float], name: str) -> None:
        self.max = max
        self.min = min
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'RoleElement':
        assert isinstance(obj, dict)
        max = from_union([from_none, from_float], obj.get("max"))
        min = from_union([from_none, from_float], obj.get("min"))
        name = from_str(obj.get("name"))
        return RoleElement(max, min, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["max"] = from_union([from_none, to_float], self.max)
        result["min"] = from_union([from_none, to_float], self.min)
        result["name"] = from_str(self.name)
        return result


class ListRoles:
    roles: List[RoleElement]

    def __init__(self, roles: List[RoleElement]) -> None:
        self.roles = roles

    @staticmethod
    def from_dict(obj: Any) -> 'ListRoles':
        assert isinstance(obj, dict)
        roles = from_list(RoleElement.from_dict, obj.get("roles"))
        return ListRoles(roles)

    def to_dict(self) -> dict:
        result: dict = {}
        result["roles"] = from_list(lambda x: to_class(RoleElement, x), self.roles)
        return result


class RoomPlayer:
    name: str
    roles: List[float]
    sid: str

    def __init__(self, name: str, roles: List[float], sid: str) -> None:
        self.name = name
        self.roles = roles
        self.sid = sid

    @staticmethod
    def from_dict(obj: Any) -> 'RoomPlayer':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        roles = from_list(from_float, obj.get("roles"))
        sid = from_str(obj.get("sid"))
        return RoomPlayer(name, roles, sid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["roles"] = from_list(to_float, self.roles)
        result["sid"] = from_str(self.sid)
        return result


class RoomElement:
    in_game: bool
    owner: str
    players: List[RoomPlayer]
    room: str

    def __init__(self, in_game: bool, owner: str, players: List[RoomPlayer], room: str) -> None:
        self.in_game = in_game
        self.owner = owner
        self.players = players
        self.room = room

    @staticmethod
    def from_dict(obj: Any) -> 'RoomElement':
        assert isinstance(obj, dict)
        in_game = from_bool(obj.get("in_game"))
        owner = from_str(obj.get("owner"))
        players = from_list(RoomPlayer.from_dict, obj.get("players"))
        room = from_str(obj.get("room"))
        return RoomElement(in_game, owner, players, room)

    def to_dict(self) -> dict:
        result: dict = {}
        result["in_game"] = from_bool(self.in_game)
        result["owner"] = from_str(self.owner)
        result["players"] = from_list(lambda x: to_class(RoomPlayer, x), self.players)
        result["room"] = from_str(self.room)
        return result


class ListRooms:
    rooms: List[RoomElement]

    def __init__(self, rooms: List[RoomElement]) -> None:
        self.rooms = rooms

    @staticmethod
    def from_dict(obj: Any) -> 'ListRooms':
        assert isinstance(obj, dict)
        rooms = from_list(RoomElement.from_dict, obj.get("rooms"))
        return ListRooms(rooms)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rooms"] = from_list(lambda x: to_class(RoomElement, x), self.rooms)
        return result


class ClientToServerResponse:
    list_roles: ListRoles
    list_rooms: ListRooms

    def __init__(self, list_roles: ListRoles, list_rooms: ListRooms) -> None:
        self.list_roles = list_roles
        self.list_rooms = list_rooms

    @staticmethod
    def from_dict(obj: Any) -> 'ClientToServerResponse':
        assert isinstance(obj, dict)
        list_roles = ListRoles.from_dict(obj.get("list_roles"))
        list_rooms = ListRooms.from_dict(obj.get("list_rooms"))
        return ClientToServerResponse(list_roles, list_rooms)

    def to_dict(self) -> dict:
        result: dict = {}
        result["list_roles"] = to_class(ListRoles, self.list_roles)
        result["list_rooms"] = to_class(ListRooms, self.list_rooms)
        return result


class RoomPlayerClass:
    name: str
    roles: List[float]
    sid: str

    def __init__(self, name: str, roles: List[float], sid: str) -> None:
        self.name = name
        self.roles = roles
        self.sid = sid

    @staticmethod
    def from_dict(obj: Any) -> 'RoomPlayerClass':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        roles = from_list(from_float, obj.get("roles"))
        sid = from_str(obj.get("sid"))
        return RoomPlayerClass(name, roles, sid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["roles"] = from_list(to_float, self.roles)
        result["sid"] = from_str(self.sid)
        return result


class Room:
    in_game: bool
    owner: str
    players: List[RoomPlayerClass]
    room: str

    def __init__(self, in_game: bool, owner: str, players: List[RoomPlayerClass], room: str) -> None:
        self.in_game = in_game
        self.owner = owner
        self.players = players
        self.room = room

    @staticmethod
    def from_dict(obj: Any) -> 'Room':
        assert isinstance(obj, dict)
        in_game = from_bool(obj.get("in_game"))
        owner = from_str(obj.get("owner"))
        players = from_list(RoomPlayerClass.from_dict, obj.get("players"))
        room = from_str(obj.get("room"))
        return Room(in_game, owner, players, room)

    def to_dict(self) -> dict:
        result: dict = {}
        result["in_game"] = from_bool(self.in_game)
        result["owner"] = from_str(self.owner)
        result["players"] = from_list(lambda x: to_class(RoomPlayerClass, x), self.players)
        result["room"] = from_str(self.room)
        return result


class Player:
    name: str
    roles: List[float]
    sid: str

    def __init__(self, name: str, roles: List[float], sid: str) -> None:
        self.name = name
        self.roles = roles
        self.sid = sid

    @staticmethod
    def from_dict(obj: Any) -> 'Player':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        roles = from_list(from_float, obj.get("roles"))
        sid = from_str(obj.get("sid"))
        return Player(name, roles, sid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["roles"] = from_list(to_float, self.roles)
        result["sid"] = from_str(self.sid)
        return result


class ServerToClient(Enum):
    GAME_ENDED = "game_ended"
    GAME_STARTED = "game_started"
    OPERATORS_AVAILABLE = "operators_available"
    OPERATOR_APPLIED = "operator_applied"
    ROLES_CHANGED = "roles_changed"
    ROOM_CHANGED = "room_changed"
    ROOM_CREATED = "room_created"
    ROOM_DELETED = "room_deleted"
    ROOM_JOINED = "room_joined"
    ROOM_LEFT = "room_left"
    TRANSITION = "transition"
    YOUR_SID = "your_sid"


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


class RoomChangedPlayer:
    name: str
    roles: List[float]
    sid: str

    def __init__(self, name: str, roles: List[float], sid: str) -> None:
        self.name = name
        self.roles = roles
        self.sid = sid

    @staticmethod
    def from_dict(obj: Any) -> 'RoomChangedPlayer':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        roles = from_list(from_float, obj.get("roles"))
        sid = from_str(obj.get("sid"))
        return RoomChangedPlayer(name, roles, sid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["roles"] = from_list(to_float, self.roles)
        result["sid"] = from_str(self.sid)
        return result


class RoomChanged:
    """Catch all event for when anything about a room state changes"""

    in_game: bool
    owner: str
    players: List[RoomChangedPlayer]
    room: str

    def __init__(self, in_game: bool, owner: str, players: List[RoomChangedPlayer], room: str) -> None:
        self.in_game = in_game
        self.owner = owner
        self.players = players
        self.room = room

    @staticmethod
    def from_dict(obj: Any) -> 'RoomChanged':
        assert isinstance(obj, dict)
        in_game = from_bool(obj.get("in_game"))
        owner = from_str(obj.get("owner"))
        players = from_list(RoomChangedPlayer.from_dict, obj.get("players"))
        room = from_str(obj.get("room"))
        return RoomChanged(in_game, owner, players, room)

    def to_dict(self) -> dict:
        result: dict = {}
        result["in_game"] = from_bool(self.in_game)
        result["owner"] = from_str(self.owner)
        result["players"] = from_list(lambda x: to_class(RoomChangedPlayer, x), self.players)
        result["room"] = from_str(self.room)
        return result


class RoomCreated:
    """A room with the given name has been created"""

    owner_sid: str
    room: str

    def __init__(self, owner_sid: str, room: str) -> None:
        self.owner_sid = owner_sid
        self.room = room

    @staticmethod
    def from_dict(obj: Any) -> 'RoomCreated':
        assert isinstance(obj, dict)
        owner_sid = from_str(obj.get("owner_sid"))
        room = from_str(obj.get("room"))
        return RoomCreated(owner_sid, room)

    def to_dict(self) -> dict:
        result: dict = {}
        result["owner_sid"] = from_str(self.owner_sid)
        result["room"] = from_str(self.room)
        return result


class RoomDeleted:
    """A room with the given name has been deleted"""

    room: str

    def __init__(self, room: str) -> None:
        self.room = room

    @staticmethod
    def from_dict(obj: Any) -> 'RoomDeleted':
        assert isinstance(obj, dict)
        room = from_str(obj.get("room"))
        return RoomDeleted(room)

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


class YourSid:
    """Inform the client of its sid"""

    sid: str

    def __init__(self, sid: str) -> None:
        self.sid = sid

    @staticmethod
    def from_dict(obj: Any) -> 'YourSid':
        assert isinstance(obj, dict)
        sid = from_str(obj.get("sid"))
        return YourSid(sid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sid"] = from_str(self.sid)
        return result


class ServerToClientEvents:
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

    room_changed: RoomChanged
    """Catch all event for when anything about a room state changes"""

    room_created: RoomCreated
    """A room with the given name has been created"""

    room_deleted: RoomDeleted
    """A room with the given name has been deleted"""

    room_joined: RoomJoined
    """A user has joined the client's room"""

    room_left: RoomLeft
    """A user has left the current client's room"""

    transition: Transition
    """A transition event has occurred for the current client's game"""

    your_sid: YourSid
    """Inform the client of its sid"""

    def __init__(self, game_ended: GameEnded, game_started: GameStarted, operator_applied: OperatorApplied, operators_available: OperatorsAvailable, roles_changed: RolesChanged, room_changed: RoomChanged, room_created: RoomCreated, room_deleted: RoomDeleted, room_joined: RoomJoined, room_left: RoomLeft, transition: Transition, your_sid: YourSid) -> None:
        self.game_ended = game_ended
        self.game_started = game_started
        self.operator_applied = operator_applied
        self.operators_available = operators_available
        self.roles_changed = roles_changed
        self.room_changed = room_changed
        self.room_created = room_created
        self.room_deleted = room_deleted
        self.room_joined = room_joined
        self.room_left = room_left
        self.transition = transition
        self.your_sid = your_sid

    @staticmethod
    def from_dict(obj: Any) -> 'ServerToClientEvents':
        assert isinstance(obj, dict)
        game_ended = GameEnded.from_dict(obj.get("game_ended"))
        game_started = GameStarted.from_dict(obj.get("game_started"))
        operator_applied = OperatorApplied.from_dict(obj.get("operator_applied"))
        operators_available = OperatorsAvailable.from_dict(obj.get("operators_available"))
        roles_changed = RolesChanged.from_dict(obj.get("roles_changed"))
        room_changed = RoomChanged.from_dict(obj.get("room_changed"))
        room_created = RoomCreated.from_dict(obj.get("room_created"))
        room_deleted = RoomDeleted.from_dict(obj.get("room_deleted"))
        room_joined = RoomJoined.from_dict(obj.get("room_joined"))
        room_left = RoomLeft.from_dict(obj.get("room_left"))
        transition = Transition.from_dict(obj.get("transition"))
        your_sid = YourSid.from_dict(obj.get("your_sid"))
        return ServerToClientEvents(game_ended, game_started, operator_applied, operators_available, roles_changed, room_changed, room_created, room_deleted, room_joined, room_left, transition, your_sid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["game_ended"] = to_class(GameEnded, self.game_ended)
        result["game_started"] = to_class(GameStarted, self.game_started)
        result["operator_applied"] = to_class(OperatorApplied, self.operator_applied)
        result["operators_available"] = to_class(OperatorsAvailable, self.operators_available)
        result["roles_changed"] = to_class(RolesChanged, self.roles_changed)
        result["room_changed"] = to_class(RoomChanged, self.room_changed)
        result["room_created"] = to_class(RoomCreated, self.room_created)
        result["room_deleted"] = to_class(RoomDeleted, self.room_deleted)
        result["room_joined"] = to_class(RoomJoined, self.room_joined)
        result["room_left"] = to_class(RoomLeft, self.room_left)
        result["transition"] = to_class(Transition, self.transition)
        result["your_sid"] = to_class(YourSid, self.your_sid)
        return result


class ServerError(Enum):
    CANT_DELETE_ROOM = "CantDeleteRoom"
    CANT_JOIN_ROOM = "CantJoinRoom"
    GAME_ALREADY_STARTED = "GameAlreadyStarted"
    GAME_NOT_STARTED = "GameNotStarted"
    INVALID_OPERATOR = "InvalidOperator"
    INVALID_ROLES = "InvalidRoles"
    NOT_IN_A_ROOM = "NotInARoom"
    RESPONSE_TIMEOUT = "ResponseTimeout"
    ROOM_ALREADY_EXISTS = "RoomAlreadyExists"


class Error:
    message: Optional[str]
    type: ServerError

    def __init__(self, message: Optional[str], type: ServerError) -> None:
        self.message = message
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Error':
        assert isinstance(obj, dict)
        message = from_union([from_none, from_str], obj.get("message"))
        type = ServerError(obj.get("type"))
        return Error(message, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message"] = from_union([from_none, from_str], self.message)
        result["type"] = to_enum(ServerError, self.type)
        return result


class ErrorResponse:
    error: Optional[Error]

    def __init__(self, error: Optional[Error]) -> None:
        self.error = error

    @staticmethod
    def from_dict(obj: Any) -> 'ErrorResponse':
        assert isinstance(obj, dict)
        error = from_union([Error.from_dict, from_none], obj.get("error"))
        return ErrorResponse(error)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.error is not None:
            result["error"] = from_union([lambda x: to_class(Error, x), from_none], self.error)
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


class SocketTypesTR:
    """For a Typescript client, your Socket can have type
    ```
    Socket<SocketTypes<ServerToClientEvents>, SocketTypes<ClientToServerEvents>>
    ```
    """
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'SocketTypesTR':
        assert isinstance(obj, dict)
        return SocketTypesTR()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


def shared_event_from_dict(s: Any) -> SharedEvent:
    return SharedEvent(s)


def shared_event_to_dict(x: SharedEvent) -> Any:
    return to_enum(SharedEvent, x)


def client_to_server_from_dict(s: Any) -> ClientToServer:
    return ClientToServer(s)


def client_to_server_to_dict(x: ClientToServer) -> Any:
    return to_enum(ClientToServer, x)


def client_to_server_events_from_dict(s: Any) -> ClientToServerEvents:
    return ClientToServerEvents.from_dict(s)


def client_to_server_events_to_dict(x: ClientToServerEvents) -> Any:
    return to_class(ClientToServerEvents, x)


def client_to_server_response_from_dict(s: Any) -> ClientToServerResponse:
    return ClientToServerResponse.from_dict(s)


def client_to_server_response_to_dict(x: ClientToServerResponse) -> Any:
    return to_class(ClientToServerResponse, x)


def room_from_dict(s: Any) -> Room:
    return Room.from_dict(s)


def room_to_dict(x: Room) -> Any:
    return to_class(Room, x)


def player_from_dict(s: Any) -> Player:
    return Player.from_dict(s)


def player_to_dict(x: Player) -> Any:
    return to_class(Player, x)


def server_to_client_from_dict(s: Any) -> ServerToClient:
    return ServerToClient(s)


def server_to_client_to_dict(x: ServerToClient) -> Any:
    return to_enum(ServerToClient, x)


def server_to_client_events_from_dict(s: Any) -> ServerToClientEvents:
    return ServerToClientEvents.from_dict(s)


def server_to_client_events_to_dict(x: ServerToClientEvents) -> Any:
    return to_class(ServerToClientEvents, x)


def error_response_from_dict(s: Any) -> ErrorResponse:
    return ErrorResponse.from_dict(s)


def error_response_to_dict(x: ErrorResponse) -> Any:
    return to_class(ErrorResponse, x)


def server_error_from_dict(s: Any) -> ServerError:
    return ServerError(s)


def server_error_to_dict(x: ServerError) -> Any:
    return to_enum(ServerError, x)


def role_from_dict(s: Any) -> Role:
    return Role.from_dict(s)


def role_to_dict(x: Role) -> Any:
    return to_class(Role, x)


def socket_types_from_dict(s: Any) -> SocketTypesTR:
    return SocketTypesTR.from_dict(s)


def socket_types_to_dict(x: SocketTypesTR) -> Any:
    return to_class(SocketTypesTR, x)


def socket_types_tr_from_dict(s: Any) -> SocketTypesTR:
    return SocketTypesTR.from_dict(s)


def socket_types_tr_to_dict(x: SocketTypesTR) -> Any:
    return to_class(SocketTypesTR, x)
