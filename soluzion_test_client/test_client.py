import argparse
import json
import threading

import socketio
from prompt_toolkit import PromptSession
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.history import InMemoryHistory

from soluzion_server.soluzion_types import *
from soluzion_test_client.parser import create_parser

# region Setup CLI args
parser = argparse.ArgumentParser(
    prog="soluzion_client",
    description="Test client for sending events to Soluzion server and playing problems text based",
    epilog="",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "host", type=str, default="localhost", help="host to connect to", nargs="?"
)
parser.add_argument("-p", "--port", type=int, default=5000, help="port to connect to")
parser.add_argument(
    "--no-connect",
    dest="noConnect",
    action="store_true",
    default=False,
    help="don't automatically connect SocketIO",
)
parser.add_argument(
    "--quickjoin",
    action="store_true",
    help="Quickly create and join a game",
)
parser.add_argument(
    "-r", "--room", type=str, default="room", help="room name to use for --quickjoin"
)
parser.add_argument(
    "-u",
    "--username",
    type=str,
    default="client",
    help="username to use for --quickjoin",
)
parser.add_argument(
    "--roles",
    type=int,
    nargs="*",
    help="roles to use for --quickjoin",
)
args = parser.parse_args()
# endregion

sio = socketio.Client()


# Simple lock to keep printed messages coherent
output_lock = threading.Lock()


# region Event Handlers


@sio.on(SharedEvent.CONNECT.value)
def connect():
    print("Connected to the server.")


@sio.on(SharedEvent.DISCONNECT.value)
def disconnect():
    print("Disconnected from the server.")


@sio.on(ClientEvent.OPERATOR_APPLIED.value)
def state_updated(data):
    event = OperatorApplied.from_dict(data)

    output_lock.acquire()
    print(event.message)
    output_lock.release()


@sio.on(ClientEvent.GAME_STARTED.value)
def state_updated(data):
    event = GameStarted.from_dict(data)

    output_lock.acquire()
    print(event.message)
    output_lock.release()


@sio.on(ClientEvent.OPERATORS_AVAILABLE.value)
def state_updated(data):
    event = OperatorsAvailable.from_dict(data)

    output_lock.acquire()
    if len(event.operators) > 0:
        for operator in event.operators:
            print(f"({int(operator.op_no)}) {operator.name}")
    else:
        print("Waiting for other players to choose operators")
    output_lock.release()


@sio.on(ClientEvent.TRANSITION.value)
def transition(data):
    event = Transition.from_dict(data)
    text = event.message

    lines = text.split("\n")

    length = max(len(line) for line in lines)

    frame_horiz = "+-" + length * "-" + "-+"

    output_lock.acquire()
    print(frame_horiz)
    for line in lines:
        print(line)
    print(frame_horiz)
    output_lock.release()


@sio.on("*")
def any_event(event, data):
    output_lock.acquire()
    print(f"\n{event} {json.dumps(data or {})}")
    output_lock.release()


# endregion


def main():
    try:
        host: str = args.host
        port: int = args.port
        if not host.startswith("http"):
            host = "http://" + host
        url = f"{host}:{port}"

        event_parser, subparsers = create_parser(ServerEvents)

        if args.noConnect:
            subparsers.add_parser(
                "connect",
                help="Connect the SocketIO client to the server",
            )
        else:
            print(f"Connecting to {url} ...")
            sio.connect(url)

        get_input = lambda: input("")

        try:
            session = PromptSession(
                history=InMemoryHistory(), cursor=CursorShape.BLINKING_BLOCK
            )
            get_input = lambda: session.prompt("")
        except:
            pass

        def print_help():
            event_parser.print_help()
            print(
                "    [operator_number]   Alias for operator_chosen --op-no [operator_number]"
            )

        print_help()

        if args.quickjoin:
            sio.emit(ServerEvent.CREATE_ROOM.value, CreateRoom(args.room).to_dict())
            sio.emit(
                ServerEvent.JOIN_ROOM.value,
                JoinRoom(args.room, args.username).to_dict(),
            )
            if args.roles is not None:
                sio.emit(ServerEvent.SET_ROLES.value, SetRoles(args.roles).to_dict())
            sio.emit(ServerEvent.START_GAME.value, {})

        while True:
            cmd = get_input().strip().split(" ")

            if len(cmd) == 0 or (len(cmd) == 1 and cmd[0] == ""):
                continue

            if cmd[0].isdigit():
                cmd = ["operator_chosen", "--op_no"] + cmd

            try:
                params = event_parser.parse_args(cmd)
                payload: dict[str, any] = vars(params)
                event = payload.pop("command")

                if event == "exit":
                    break

                if event == "help":
                    print_help()
                    continue

                if event == "connect":
                    print(f"Connecting to {url} ...")
                    sio.connect(url)
                    continue

                response = sio.emit(event, payload)

                if response is not None:
                    print(response)

            except Exception as e:
                if str(e) != "help":
                    print(e)

    except KeyboardInterrupt:
        return
    except EOFError:
        return
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        sio.disconnect()


if __name__ == "__main__":
    main()
