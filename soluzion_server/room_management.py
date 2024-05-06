from flask import request
from flask_socketio import emit, SocketIO, join_room, leave_room

from soluzion_server.globals import *
from soluzion_server.globals import RoomSession, PlayerSession
from soluzion_server.soluzion_types import *


def configure_room_handlers(socketio: SocketIO):
    @socketio.on(SharedEvent.CONNECT.value)
    def handle_connect():
        """
        When a client establishes the socket connection
        """
        print("Client connected:", request.sid)
        connected_players[request.sid] = PlayerSession(request.sid, None, None, set())

    @socketio.on(SharedEvent.DISCONNECT.value)
    def handle_disconnect():
        """
        When a client disconnects the socket connection
        """

        print("Client disconnected:", request.sid)

        # TODO more disconnect handling

        del connected_players[request.sid]

    @socketio.on(ServerEvent.CREATE_ROOM.value)
    def create_room(data):
        event = CreateRoom.from_dict(data)

        if event.room in room_sessions:
            emit(
                ClientEvent.ERROR.value,
                Error(
                    ServerError.ROOM_ALREADY_EXISTS, ServerEvent.CREATE_ROOM, None
                ).to_dict(),
            )
            return

        room_sessions[event.room] = RoomSession(event.room, request.sid, [], None)

        emit(
            ClientEvent.ROOM_CREATED.value,
            RoomCreated(event.room).to_dict(),
            broadcast=True,
        )

    @socketio.on(ServerEvent.JOIN_ROOM.value)
    def on_join_room(data):
        event = JoinRoom.from_dict(data)

        if event.room not in room_sessions:
            emit(
                ClientEvent.ERROR.value,
                Error(
                    ServerError.CANT_JOIN_ROOM,
                    ServerEvent.JOIN_ROOM,
                    "Room Does Not Exist",
                ).to_dict(),
            )
            return

        player: PlayerSession = current_player(request.sid)

        if player.room is not None:
            emit(
                ClientEvent.ERROR.value,
                Error(
                    ServerError.CANT_JOIN_ROOM,
                    ServerEvent.JOIN_ROOM,
                    "Already in another Room",
                ).to_dict(),
            )
            return

        room: RoomSession = room_sessions[event.room]

        player.room = room.id
        player.name = event.username

        join_room(room.id)
        room.player_sids.append(request.sid)

        emit(
            ClientEvent.ROOM_JOINED.value,
            RoomJoined(event.username).to_dict(),
            to=room.id,
        )

    @socketio.on(ServerEvent.LEAVE_ROOM.value)
    def on_leave_room(data):
        room = current_room(request.sid)
        player: PlayerSession = current_player(request.sid)

        if room is None or player.room is None:
            emit(
                ClientEvent.ERROR.value,
                Error(
                    ServerError.NOT_IN_A_ROOM,
                    ServerEvent.LEAVE_ROOM,
                    "You are not in a room",
                ).to_dict(),
            )
            return

        username = player.name
        player.room = None
        player.name = None
        player.role = None

        leave_room(room.id)
        room.player_sids.remove(request.sid)

        emit(ClientEvent.ROOM_LEFT.value, RoomLeft(username).to_dict(), to=room.id)

    @socketio.on(ServerEvent.SET_NAME.value)
    def on_set_name(data):
        event = SetName.from_dict(data)
        player: PlayerSession = current_player(request.sid)
        player.name = event.name

        # TODO name updated event

    @socketio.on(ServerEvent.SET_ROLES.value)
    def on_add_role(data):
        event = SetRoles.from_dict(data)
        room = current_room(request.sid)
        player = current_player(request.sid)

        if room is None or player.room is None:
            emit(
                ClientEvent.ERROR.value,
                Error(
                    ServerError.NOT_IN_A_ROOM,
                    ServerEvent.SET_ROLES,
                    "You are not in a room",
                ).to_dict(),
            )
            return

        player.roles.clear()
        player.roles.update(map(int, event.roles))

        emit(
            ClientEvent.ROLES_CHANGED.value,
            RolesChanged(list(player.roles), player.name).to_dict(),
            to=room.id,
        )
