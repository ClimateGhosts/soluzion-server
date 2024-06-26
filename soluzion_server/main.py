import argparse

from flask import Flask, jsonify
from flask_cors import CORS
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
parser.add_argument("-d", "--debug", action="store_true", help="enable debug mode")
args = parser.parse_args()

# Load the passed in Soluzion problem
load_problem(args.problem_path)

# Only import these after the problem has been loaded
from soluzion_server.room_management import configure_room_handlers
from soluzion_server.game_management import configure_game_handlers

# Configure the flask socketio server
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, logger=args.debug, cors_allowed_origins="*")
cors = CORS(app, resources={r"*": {"origins": "*"}})

# Add the handlers for processing player/room joining
configure_room_handlers(socketio)

# Add the handlers for processing game events
configure_game_handlers(socketio)


# Health Endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


def main():
    """Start the Soluzion Server"""
    socketio.run(
        app,
        host="0.0.0.0",
        port=args.port,
        debug=args.debug,
        allow_unsafe_werkzeug=True,
    )


if __name__ == "__main__":
    main()
