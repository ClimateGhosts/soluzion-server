import json

import socketio

from soluzion_server.soluzion_types import *

sio = socketio.Client()


@sio.on(SharedEvent.CONNECT.value)
def connect():
    print("Connected to the server.")


@sio.on(SharedEvent.DISCONNECT.value)
def disconnect():
    print("Disconnected from the server.")


@sio.on(ClientEvent.OPERATOR_APPLIED.value)
def state_updated(data):
    event = OperatorApplied.from_dict(data)

    print(event.message)


@sio.on(ClientEvent.GAME_STARTED.value)
def state_updated(data):
    event = GameStarted.from_dict(data)

    print(event.message)


@sio.on(ClientEvent.OPERATORS_AVAILABLE.value)
def state_updated(data):
    event = OperatorsAvailable.from_dict(data)

    if len(event.operators) > 0:
        for operator in event.operators:
            print(f"({int(operator.op_no)}) {operator.name}")
    else:
        print("Waiting for other players to choose operators")


@sio.on(ClientEvent.TRANSITION.value)
def transition(data):
    event = Transition.from_dict(data)
    text = event.message

    lines = text.split("\n")

    length = max(len(line) for line in lines)

    frame_horiz = "+-" + length * "-" + "-+"
    print(frame_horiz)
    for line in lines:
        print(line)
    print(frame_horiz)


@sio.on("*")
def any_event(event, data):
    print(f"\n{event} {json.dumps(data or {})}")


def main():
    try:
        sio.connect("http://localhost:5000")
        print(
            "SocketIO Client is running. Commands are 'exit', 'create', 'join', 'start'"
        )

        while True:
            cmd = input("").strip().lower()
            if cmd == "exit":
                break
            elif cmd == "create":
                # room_name = input("Enter room name to create: ")
                sio.emit(ServerEvent.CREATE_ROOM.value, CreateRoom("room").to_dict())
            elif cmd == "join":
                # room_name = input("Enter room name to join: ")
                # username = input("Enter username to use: ")
                sio.emit(
                    ServerEvent.JOIN_ROOM.value,
                    JoinRoom("room", "room").to_dict(),
                )
            elif cmd == "roles":
                sio.emit(ServerEvent.SET_ROLES.value, SetRoles([0, 1, 2, 3]).to_dict())
            elif cmd == "start":
                sio.emit(ServerEvent.START_GAME.value, {})
            else:
                operator = int(cmd)
                sio.emit(
                    ServerEvent.OPERATOR_CHOSEN.value,
                    OperatorChosen(operator, None).to_dict(),
                )

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        sio.disconnect()


if __name__ == "__main__":
    main()
