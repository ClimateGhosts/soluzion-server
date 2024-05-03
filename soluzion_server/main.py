from flask import Flask
from flask_socketio import SocketIO

# Load the passed in Soluzion problem
from soluzion_server.problem_loading import load_problem

load_problem()

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
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)


if __name__ == "__main__":
    main()
