from datetime import datetime


def parse_players(player: dict) -> dict:

    try:
        team_name = player["team"]["name"]
    except Exception:
        team_name = None

    try:
        delivery_city = player["team"]["city"]
    except Exception:
        delivery_city = None

    first_name = player["first_name"] if "first_name" in player else None
    last_name = player["last_name"] if "last_name" in player else None

    if first_name and last_name and team_name:
        email = f"{first_name.lower()}.{last_name.lower()}@{team_name.lower()}.com"
    else:
        email = None

    return {
        "id": str(player["id"]) if "id" in player else None,
        "created_at": datetime(2022, 11, 7),
        "updated_at": datetime.now(),
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "team_name": team_name,
        "delivery_city": delivery_city
    }
