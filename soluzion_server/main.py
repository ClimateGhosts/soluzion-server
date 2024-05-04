import argparse

from flask import Flask
from flask_socketio import SocketIO

from soluzion_server.problem_loading import load_problem

# Setup CLI args
parser = argparse.ArgumentParser(
    prog="soluzion_server",
    description="",
    epilog="",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("problem_path", type=str, help="Path to the Soluzion problem file")
parser.add_argument("-p", "--port", type=int, default=5000, help="port to listen on")
args = parser.parse_args()

# Load the passed in Soluzion problem
load_problem(args.problem_path)

# Only import these after the problem has been loaded
from soluzion_server.room_management import configure_room_handlers
from soluzion_server.game_management import configure_game_handlers

# Configure the flask socketio server
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

# Add the handlers for processing player/room joining
configure_room_handlers(socketio)

# Add the handlers for processing game events
configure_game_handlers(socketio)


def main():
    """
    Start the Soluzion Server
    """
    socketio.run(app, port=args.port, debug=True, allow_unsafe_werkzeug=True)


if __name__ == "__main__":
    main()
