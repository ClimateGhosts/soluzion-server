from flask import request
from flask_socketio import emit, SocketIO, join_room, leave_room

from soluzion_server.globals import *
from soluzion_server.globals import RoomSession, PlayerSession
from soluzion_server.soluzion_types import *
from importlib.metadata import version


def configure_room_handlers(socketio: SocketIO):
    @socketio.on(ClientToServer.INFO.value)
    def info(data):
        return Info(
            getattr(PROBLEM, "PROBLEM_AUTHORS", []),
            getattr(PROBLEM, "PROBLEM_CREATION_DATE", ""),
            getattr(PROBLEM, "PROBLEM_DESC", ""),
            getattr(PROBLEM, "PROBLEM_NAME", ""),
            getattr(PROBLEM, "PROBLEM_VERSION", ""),
            version("soluzion_server"),
            getattr(PROBLEM, "SOLUZION_VERSION", ""),
        ).to_dict()

    @socketio.on(SharedEvent.CONNECT.value)
    def handle_connect():
        """
        When a client establishes the socket connection
        """
        print("Client connected:", request.sid)
        connected_players[request.sid] = PlayerSession(request.sid, None, None, set())

        emit(
            ServerToClient.YOUR_SID.value,
            YourSid(request.sid).to_dict(),
            to=request.sid,
        )

    @socketio.on(SharedEvent.DISCONNECT.value)
    def handle_disconnect():
        """
        When a client disconnects the socket connection
        """

        print("Client disconnected:", request.sid)

        # TODO more disconnect handling
        room = current_room(request.sid)

        if room is not None:
            room.player_sids.remove(request.sid)

            if len(room.player_sids) == 0:
                print(f"Everyone has left the game in room {room.id}, deleting")
                room.game = None
                del room_sessions[room.id]
                emit(
                    ServerToClient.ROOM_DELETED.value,
                    RoomDeleted(room.id).to_dict(),
                    broadcast=True,
                )

            elif room.owner_sid == request.sid:
                room.owner_sid = room.player_sids[0]

        del connected_players[request.sid]

    @socketio.on(ClientToServer.CREATE_ROOM.value)
    def on_create_room(data):
        event = CreateRoom.from_dict(data)

        if event.room in room_sessions:
            return error_response(ServerError.ROOM_ALREADY_EXISTS)

        room_sessions[event.room] = RoomSession(event.room, request.sid, [], None)

        emit(
            ServerToClient.ROOM_CREATED.value,
            RoomCreated(request.sid, event.room).to_dict(),
            broadcast=True,
        )

    @socketio.on(ClientToServer.DELETE_ROOM.value)
    def on_create_room(data):
        event = DeleteRoom.from_dict(data)

        if event.room not in room_sessions:
            return error_response(ServerError.CANT_DELETE_ROOM, "Room does not exist")

        room = room_sessions[event.room]

        if len(room.player_sids) > 0:
            return error_response(ServerError.CANT_DELETE_ROOM, "Room not empty")

        # if room.owner_sid != request.sid:
        #     return error_response(ServerError.CANT_DELETE_ROOM, "You are not the owner")

        del room_sessions[event.room]

        emit(
            ServerToClient.ROOM_DELETED.value,
            RoomDeleted(event.room).to_dict(),
            broadcast=True,
        )

    @socketio.on(ClientToServer.JOIN_ROOM.value)
    def on_join_room(data):
        print("Join room is ", data)
        event = JoinRoom.from_dict(data)

        if event.room not in room_sessions:
            return error_response(ServerError.CANT_JOIN_ROOM, "Room Does Not Exist")

        player: PlayerSession = current_player(request.sid)

        if player.room is not None:
            return error_response(ServerError.CANT_JOIN_ROOM, "Already in another Room")

        room: RoomSession = room_sessions[event.room]

        player.room = room.id
        player.name = event.username

        join_room(room.id)
        room.player_sids.append(request.sid)

        if len(room.player_sids) == 1:
            room.owner_sid = request.sid

        emit(
            ServerToClient.ROOM_JOINED.value,
            RoomJoined(event.username).to_dict(),
            to=room.id,
        )
        emit(ServerToClient.ROOM_CHANGED.value, room.to_dict(), broadcast=True)

    @socketio.on(ClientToServer.LEAVE_ROOM.value)
    def on_leave_room(data):
        room = current_room(request.sid)
        player: PlayerSession = current_player(request.sid)

        if room is None or player.room is None:
            return error_response(ServerError.NOT_IN_A_ROOM)

        username = player.name
        player.room = None
        player.name = None
        player.role = None

        leave_room(room.id)
        room.player_sids.remove(request.sid)

        emit(ServerToClient.ROOM_LEFT.value, RoomLeft(username).to_dict(), to=room.id)
        emit(ServerToClient.ROOM_CHANGED.value, room.to_dict(), broadcast=True)

    @socketio.on(ClientToServer.SET_NAME.value)
    def on_set_name(data):
        event = SetName.from_dict(data)
        player: PlayerSession = current_player(request.sid)
        player.name = event.name

        # TODO name updated event

        if player.room is not None:
            room = current_room(request.sid)
            emit(ServerToClient.ROOM_CHANGED.value, room.to_dict(), broadcast=True)

    @socketio.on(ClientToServer.SET_ROLES.value)
    def on_set_roles(data):
        event = SetRoles.from_dict(data)
        room = current_room(request.sid)
        player = current_player(request.sid)

        if room is None or player.room is None:
            return error_response(ServerError.NOT_IN_A_ROOM)

        player.roles.clear()
        player.roles.update(map(int, event.roles))

        emit(
            ServerToClient.ROLES_CHANGED.value,
            RolesChanged(list(player.roles), player.name).to_dict(),
            to=room.id,
        )

        emit(ServerToClient.ROOM_CHANGED.value, room.to_dict(), broadcast=True)

    @socketio.on(ClientToServer.LIST_ROOMS.value)
    def on_list_rooms(data):
        return ListRooms(
            [RoomElement.from_dict(room.to_dict()) for room in room_sessions.values()]
        ).to_dict()

    @socketio.on(ClientToServer.LIST_ROLES.value)
    def on_list_rooms(data):
        try:
            return ListRoles(
                [RoleElement.from_dict(role) for role in PROBLEM.ROLES or []]
            ).to_dict()
        except Error:
            return error_response(ServerError.INVALID_ROLES)
