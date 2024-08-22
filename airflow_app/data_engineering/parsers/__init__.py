import os
import importlib
from inspect import isfunction


def get_parsing_functions(source: str) -> dict:
    # Initialize an empty dictionary to hold the parsing functions
    PARSING_FUNCTIONS = {}

    # Get the directory where this script is located
    parsers_dir = os.path.dirname(__file__) + f"/{source}"

    # Iterate over all Python files in the directory
    for filename in os.listdir(parsers_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]  # Remove the .py extension to get the module name

            # Import the module dynamically
            module = importlib.import_module(f".{module_name}", package=f"data_engineering.parsers.{source}")

            # Automatically find and register parsing functions
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isfunction(attr) and attr_name.startswith("parse_"):
                    # Assuming the convention is parse_<collection_name>
                    collection_name = attr_name.split("parse_")[1]
                    PARSING_FUNCTIONS[collection_name] = attr

    return PARSING_FUNCTIONS
