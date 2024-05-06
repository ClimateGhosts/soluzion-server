import argparse
import inspect
from typing import get_type_hints, Optional, get_origin, get_args, Union, List


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise Exception(message)


# Custom help action that does not exit the program
class CustomHelpAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        raise Exception("help")


defaults = {
    "room": "room",
    "name": "client",
    "username": "client",
}


def add_arguments_for_class(parser, cls):
    type_hints = get_type_hints(cls)
    used_short_options = set()  # Keep track of used short options to avoid conflicts

    for field, field_type in type_hints.items():
        origin = get_origin(field_type)
        args = get_args(field_type)
        if origin is Optional or origin is Union:
            required = False
            field_type = args[0]  # Unwrap the actual type from Optional[Type]
        else:
            required = True

        # Generate a short option
        short_option = f"-{field[0]}"
        if short_option in used_short_options:
            # If the short option is already used, generate an alternative
            for i in range(1, len(field)):
                short_option = f"-{field[i]}"
                if short_option not in used_short_options:
                    break
        used_short_options.add(short_option)  # Mark this short option as used

        nargs = None
        arg_type = field_type

        # Check for list types and handle them
        if origin is list or origin is List:
            element_type = args[0]
            nargs = "+"
            arg_type = element_type

        parser.add_argument(
            short_option,
            f"--{field}",
            type=arg_type,
            nargs=nargs,
            help=f"{field} ({field_type})",
            required=required and field not in defaults,
            default=defaults.get(field),
        )


def create_parser(base_class):
    # Create the main parser
    parser = CustomArgumentParser(
        prog="",
        description="Send Events to Soluzion Server",
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, parser_class=CustomArgumentParser
    )

    subparsers.add_parser("help", help="Show help for commands")
    subparsers.add_parser("exit", help="Shut down the client")

    # Create subparsers for each class in ServerEvents
    for key, cls_type in base_class.__annotations__.items():
        subparser = subparsers.add_parser(
            key,
            help=cls_type.__doc__
            or f"Request to {key.split('_')[0]} the {key.split('_')[1]}",
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        subparser.add_argument(
            "-h", "--help", action=CustomHelpAction, default=argparse.SUPPRESS, nargs=0
        )
        if inspect.isclass(cls_type):
            add_arguments_for_class(subparser, cls_type)

    return parser, subparsers
