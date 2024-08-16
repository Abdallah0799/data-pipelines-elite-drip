from typing import List
import settings

def get_data_types_to_fetch(
        source: str,
        database: str
) -> List[str]:
    """
    """
    data_to_fetch = settings.data_to_fetch

    return data_to_fetch[source][database]
