# soluzion_server

This is a restructured implementation of a Flask + SocketIO server for use with Soluzion framework problems, with an
emphasis on supporting custom clients.

## Installation

Python 3.9 or higher is required

### Direct Install

```shell
pip install git+https://github.com/ClimateGhosts/soluzion-server@main
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

### Test Client

```
soluzion_client [-h] [host] [port]

positional arguments:
  host        host to connect to (default: localhost)
  port        port to connect to (default: 5000)

optional arguments:
  -h, --help  show this help message and exit
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
