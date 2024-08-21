import os
import json
import base64

MONGO_CONNECTION_PASSWORD = os.environ["MONGO_CONNECTION_PASSWORD"]

BALLDONTLIE_API_KEY = os.environ["BALLDONTLIE_API_KEY"]

mongo_db = {
    "CONNECTION_STRING": (
        "mongodb+srv://tornadogazal:"
        f"{MONGO_CONNECTION_PASSWORD}"
        "@cluster0.ts5b0pi.mongodb.net/?retryWrites=true"
        "&w=majority&appName=Cluster0"
    )
}

SERVICE_ACCOUNT_BQ_ADMIN = json.loads(
    base64.b64decode(os.environ["SERVICE_ACCOUNT_BQ_ADMIN"])
)
SERVICE_ACCOUNT_STORAGE_ADMIN = json.loads(
    base64.b64decode(os.environ["SERVICE_ACCOUNT_STORAGE_ADMIN"])
)

AWS_S3_ACCESS_KEY = os.environ["AWS_S3_ACCESS_KEY"]

AWS_S3_ACCESS_SECRET = os.environ["AWS_S3_ACCESS_SECRET"]

MONGO_DB_FETCH_WINDOW = 1000  # days

S3_FETCH_WINDOW = 100  # days

data_to_fetch = {
    "mongodb": {
        "center": {
            "orders": {"duplicate_columns": ["id"], "order_columns": ["updated_at"]},
            "charges": {"duplicate_columns": ["id"], "order_columns": ["updated_at"]},
        }
    },
    "s3": {
        "fictive-company": {
            "order_items": {
                "duplicate_columns": ["id"],
                "order_columns": ["updated_at"],
            },
            "products": {
                "duplicate_columns": ["id"],
                "order_columns": ["updated_at"],
            },
        }
    },
    "balldontlie": {
        "nba": {
            "players": {"duplicate_columns": ["id"], "order_columns": ["updated_at"]}
        }
    },
}
