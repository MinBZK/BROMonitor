import os
import logging
from pymongo import MongoClient

from etl.extract.gld_extractor import GLDExtractor
from etl.extract.source_processor import process_geopackage
from common.config import date_format, logging_format
from etl.configuration.config import init_registration_types, registration_types
from dotenv import load_dotenv
from etl.extract.index_bronhouders import index_bronhouders
from etl.load.mongodb.mongo_helpers import initiliaze_source_document

load_dotenv()

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format=logging_format, datefmt=date_format
)
log = logging.getLogger(__name__)

mongoUrl = os.environ.get("mongodbUrl")
client = MongoClient(mongoUrl)
db = client.bro

init_registration_types()

for reg_type in registration_types:
    initiliaze_source_document(db, doc_type=reg_type.type_name)        
    process_geopackage(reg_type)

log.info("Recreating the bronhouder collection")
db.bronhouder.drop()
index_bronhouders()
gld_extractor = GLDExtractor()
gld_extractor.extract()
