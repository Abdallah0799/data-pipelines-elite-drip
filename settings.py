import os
import json
import base64

MONGO_CONNECTION_PASSWORD = os.environ["MONGO_CONNECTION_PASSWORD"]

mongo_db = {
    "CONNECTION_STRING": ("mongodb+srv://tornadogazal:"
                          f"{MONGO_CONNECTION_PASSWORD}"
                          "@cluster0.ts5b0pi.mongodb.net/?retryWrites=true"
                          "&w=majority&appName=Cluster0")
}

SERVICE_ACCOUNT_BQ_ADMIN = json.loads(base64.b64decode(os.environ['SERVICE_ACCOUNT_BQ_ADMIN']))
