import os
import importlib

# Directory where schema Python files are stored
SCHEMA_DIR = os.path.dirname(__file__)


def load_schema(schema_name):
    """
    Load a BigQuery schema from a Python module.

    :param schema_name: Name of the schema (without file extension).
    :return: A list of bigquery.SchemaField objects representing the schema.
    :raises: ImportError if the schema module does not exist.
    """
    try:
        # Dynamically import the schema module
        module = importlib.import_module(f"data_engineering.data_schemas.bigquery")

        # Retrieve the schema list (assuming the convention <schema_name>_schema)
        schema = getattr(module, f"{schema_name}")

        return schema
    except ImportError:
        raise ValueError(f"Schema module '{schema_name}' not found.")
    except AttributeError:
        raise ValueError(f"Schema '{schema_name}_schema' not defined in module '{schema_name}'.")
