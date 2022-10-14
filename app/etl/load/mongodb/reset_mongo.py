import os
import logging
from pymongo import MongoClient

IGNORE_LIST = ["bronhouder", "search", "bromonitor", "metadata", "pageVisits", "geotop"]


def reset_mongo():
    log = logging.getLogger(__name__)
    log.info("Resetting mongoDb collections")

    mongoUrl = os.environ.get('mongodbUrl')
    client = MongoClient(mongoUrl)
    db = client.bro
    for c in db.collection_names():
        if c not in IGNORE_LIST:
            db[c].drop()
