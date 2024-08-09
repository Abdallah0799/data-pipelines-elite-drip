from dataclasses import dataclass
from typing import ClassVar


@dataclass
class BaseSchema():
    """
    from_db: gives us the database where the schema comes from
    source_name: gives us the exact name of the source (for example
    table name for relationnal databases)
    """
    from_db: ClassVar[str]
    source_name: ClassVar[str]
