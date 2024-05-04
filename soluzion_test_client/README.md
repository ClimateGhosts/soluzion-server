# soluzion_test_client

This is a minimal text based testing client for the Soluzion server. 

## Usage

```shell
pip install .
```

```
soluzion_client [-h] [-p PORT] [--no-connect] [--quickjoin] [-r ROOM] [-u USERNAME] [--roles [ROLES ...]] [host]

Test client for sending events to Soluzion server and playing problems text based

positional arguments:
  host                  host to connect to (default: localhost)

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to connect to (default: 5000)
  --no-connect          don't automatically connect SocketIO (default: False)
  --quickjoin           Quickly create and join a game (default: False)
  -r ROOM, --room ROOM  room name to use for --quickjoin (default: room)
  -u USERNAME, --username USERNAME
                        username to use for --quickjoin (default: client)
  --roles [ROLES ...]   roles to use for --quickjoin (default: None)

```

Or `python test_client.py` if you haven't pip installed this package

While running, send events using the commands

```
usage: {help,exit,create_room,join_room,leave_room,operator_chosen,set_name,set_roles,start_game,connect} ...

Send Events to Soluzion Server

positional arguments:
  {help,exit,create_room,join_room,leave_room,operator_chosen,set_name,set_roles,start_game,connect}
    help                Show help for commands
    exit                Shut down the client
    create_room         Request for the server to create a new room
    join_room           Request for the sender to join an existing room, optionally setting a username
    leave_room          Request to leave the room
    operator_chosen     Request for a specific operator to be replied within the sender's game session
    set_name            Request to set the sender's username
    set_roles           Request to set the sender's roles
    start_game          Request to start the game
    connect             Connect the SocketIO client to the server
    [operator_number]   Alias for operator_chosen --op-no [operator_number]
```

### Quick Join