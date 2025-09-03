import os
import datetime

from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")


def upload_interface(ip, status):
    client = MongoClient(MONGO_URI)
    database = client[DB_NAME]
    interface = database["interface_status"]

    current = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = interface.insert_one(
        {"router_ip": ip, "timestamp": current, "interfaces": status}
    )

    return result
