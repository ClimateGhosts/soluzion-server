# soluzion_server

This is a restructured implementation of a Flask + SocketIO server for use with Soluzion framework problems, with an
emphasis on supporting custom clients.

## Installation

Python 3.9 or higher is required

### Direct Install

```shell
pip install -U git+https://github.com/ClimateGhosts/soluzion-server@main
```

### requirements.txt or setup.py entry

```
soluzion-server @ git+https://github.com/ClimateGhosts/soluzion-server@main
```

## Usage

### Server

```
soluzion_server [-h] [-p PORT] problem_path

positional arguments:
  problem_path          Path to the Soluzion problem file

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to listen on (default: 5000)
```

e.g.
```shell
soluzion_server problems/earth-health-game.py -p 4242
```

### Test Client

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

e.g.
```shell
soluzion_client tempura.cs.washington.edu -p 4242 --quickjoin --roles 0 1 2 3
```

## Developing Clients

### Examples

See `soluzion_test_client/text_client.py` for an example of a minimal text based client written in Python.

### Types

The `soluzion_types` directory contains a simple setup for
the [`quicktype`](https://github.com/glideapps/quicktype#readme) framework to generate types for the Soluzion Server
event payloads in any language. The primary copy of the types is `soluzion-types.ts`, which can be used for
Typescript. See the `soluzion_types/output` folder for other pre-generated ones.

### Events

Looking through `soluzion_types/soluzion-types.ts` is the easiest way to get a sense of what events need to be handled
and sent by a client.

SocketIO handlers should be made for events within `ClientEvents`, while stuff in `ServerEvents` should be `.emit(...)`ed to
the server by your client.
