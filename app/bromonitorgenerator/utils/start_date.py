from pymongo import MongoClient
from datetime import datetime, timedelta
from common.config import MONGODB_URL
import requests
import json

from bromonitorgenerator.utils.utils import API_BASE


def get_start_date():
    with MongoClient(MONGODB_URL) as client:
        db = client.bro
        query = db.metadata.find_one(filter={"type": "last_bromonitor_object_date"})
        if query is not None:
            date = datetime.fromisoformat(query["value"])
        else:
            date = datetime.now() - timedelta(days=7)
        return date


def get_new_start_date():
    response = requests.get(API_BASE + f"/rapporten/laatste-registratiedatum")
    date = json.loads(response.content).get("date", None)
    fallback = datetime.now() - timedelta(days=7)
    return date if date else fallback.isoformat()


def set_start_date():
    date = get_new_start_date()
    with MongoClient(MONGODB_URL) as client:
        db = client.bro
        new_value = {"type": "last_bromonitor_object_date", "value": date}
        db.metadata.replace_one(
            filter={"type": "last_bromonitor_object_date"},
            replacement=new_value,
            upsert=True,
        )
