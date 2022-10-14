import logging
from dateutil import parser
from pymongo import MongoClient, GEOSPHERE

log = logging.getLogger(__name__)


def initiliaze_source_document(db, doc_type, name="pdok"):
    
    source_doc = db.source.find_one({"type": doc_type})
    required_keys = ['updated', 'name']
    source_doc_initialized = source_doc is not None and all([key in source_doc for key in required_keys])    

    if not source_doc_initialized:
        db.source.update_one({"type": doc_type},
                            {"$set": {"name": name,
                                    "status": "OK",
                                    "updated":  parser.parse('2000-01-01T00:00:00.000+00:00'),
                                    "last_extracted": parser.parse('2000-01-01T00:00:00.000+00:00'),
                                    "last_loaded": parser.parse('2000-01-01T00:00:00.000+00:00'),
                                    }},
                            upsert=True)


def create_indexes(db):
    log.info("Creating indexes for the common collection")
    db.common.create_index([("common.deliveredLocation.pos", 1)])
    db.common.create_index(
        [("common.deliveryAccountableParty", 1), ("common.type", 1)])
    db.common.create_index(([("common.geojson", GEOSPHERE)]))

    log.info("Creating indexes for the BHR collection")
    db.specificBHR.create_index([("surveyPurpose", 1)])
    db.specificBHR.create_index([("broId", 1)])

    log.info("Creating indexes for the CPT collection")
    db.specificCPT.create_index([("surveyPurpose", 1)])
    db.specificCPT.create_index([("broId", 1)])

    log.info("Creating indexes for the GMW collection")
    db.specificGMW.create_index([("broId", 1)])
