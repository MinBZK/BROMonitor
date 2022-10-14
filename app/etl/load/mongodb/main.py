import os
import logging
from pymongo import MongoClient

from common.config import date_format, logging_format
from etl.configuration.config import init_registration_types, registration_types
from etl.load.mongodb.gld_loader import GLDLoader
from etl.load.mongodb.mongo_helpers import create_indexes
from etl.load.mongodb.materialized_views import update_materialized_views
from etl.load.mongodb.geopackage_processor import GeopackageProcessor
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format=logging_format, datefmt=date_format
)
log = logging.getLogger(__name__)

mongoUrl = os.environ.get("mongodbUrl")
client = MongoClient(mongoUrl)
db = client.bro

try:
    # Init registration types
    init_registration_types()

    # Load GLDS
    try:
        gld_loader = GLDLoader()
        gld_loader.load()
    except Exception as e:
        log.error(
            f"Exception occured during the processing of XMLS for GLD. Error message: {str(e)}"
        )
        db.source.update_one(
            {"type": "gld"}, {"$set": {"status": "Failed loading"}}, upsert=True
        )

    # Process geopackages
    for doc_type in registration_types:
        try:
            processor = GeopackageProcessor(db, doc_type)
            processor.process()
        except Exception as e:
            log.error(
                f"Exception occured during the processing of GeoPackage for {doc_type.type_name}. Error message: {str(e)}"
            )
            db.source.update_one(
                {"type": doc_type.type_name},
                {"$set": {"status": "Failed loading"}},
                upsert=True,
            )
            continue

    create_indexes(db)
    log.info("Done creating indexes")

    update_materialized_views(db)
    log.info("Done updating materialized views")

except Exception as e:
    log.error(str(e))
