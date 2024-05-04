import os
import sys
from importlib.util import spec_from_file_location, module_from_spec

import soluzion_server.globals as server_globals


def load_problem(problem_path: str):
    """
    Loads the Soluzion problem passed in the cli args
    :return: the Soluzion problem module
    """
    if not problem_path.endswith(".py"):
        problem_path += ".py"

    problem_path = os.path.abspath(problem_path)

    if not os.path.exists(problem_path):
        print(f"Unable to find Soluzion problem file at {problem_path}")
        exit(1)

    dir_name = os.path.dirname(problem_path)

    if dir_name not in sys.path:
        sys.path.insert(0, dir_name)

    problem = server_globals.PROBLEM = load_module(problem_path)

    print(f"Successfully loaded Soluzion Problem {problem_path}")

    return problem


def load_module(path: str):
    """
    Loads a python module from a file, adjusting the working directory as needed
    :param path: path to python file
    :return: the loaded module
    """

    original_cwd = os.getcwd()
    full_path = os.path.abspath(path)

    module_name = os.path.splitext(os.path.basename(full_path))[0]

    try:
        # Change working dir name in case they do any relative file imports
        os.chdir(os.path.dirname(full_path))

        spec = spec_from_file_location(module_name, full_path)

        module = module_from_spec(spec)

        spec.loader.exec_module(module)

        return module

    finally:
        # Restore the original working directory
        os.chdir(original_cwd)
