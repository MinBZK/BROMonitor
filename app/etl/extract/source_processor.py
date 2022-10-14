from datetime import datetime
from zipfile import ZipFile
from pymongo import MongoClient
import os
import logging
import pytz

from etl.extract.feed_service import fetch_geopackage_feed
from etl.extract.feed_service import download_zip
from etl.load.mongodb.mongo_helpers import initiliaze_source_document

log = logging.getLogger(__name__)


def unzip(path, to_path, to_filename):
    with ZipFile(path, allowZip64=True) as zf:
        zf.extract(to_filename, to_path)


def process_geopackage(reg_type):
    doc_type = reg_type.type_name
    log.info("Collecting for type: '%s'" % doc_type)

    try:
        mongoUrl = os.environ.get('mongodbUrl')
        client = MongoClient(mongoUrl)
        db = client.bro
    except Exception as e:
        log.error(str(e))
        return

    # Get geopackage ATOM feed based on source URL
    try:
        source_url = os.environ.get(reg_type.sourceKey)
        feed = fetch_geopackage_feed(source_url)
        db.source.update_one({"type": doc_type}, {
                             "$set": {"last_extracted": datetime.now()}}, upsert=True)
    except Exception as e:
        log.error(str(e))
        db.source.update_one({"type": doc_type}, {
                             "$set": {"status": "Failed extracting xml"}}, upsert=True)
        return

    # Download and process ZIP from source
    try:
        source = db.source.find_one({"type": doc_type})
        log.info("Datum in feed: %s en laatst update datum: %s." %
                 (feed.updated, source['updated']))

        download_data = feed.updated > pytz.utc.localize(source['updated'])

        if download_data:
            
            download_location = os.environ.get('downloadLocation', '/mnt/brodata/')
            path = download_location + feed.filename

            log.info("Start download van %s naar %s" % (feed.zip_url, path))
            if download_zip(feed.zip_url, path):
                unzip_filename = feed.filename.replace('zip', 'gpkg')
                log.info("Unzipping %s" % path)
                if doc_type == "bhr-gt":
                    unzip_filename = "brobhrgtvolledigeset.gpkg"
                unzip_location = os.environ.get('unzipLocation', '/mnt/brodata/')                
                unzip(path, unzip_location, unzip_filename)

                db.source.update_one({"type": doc_type},
                                     {"$set": {"updated": feed.updated,
                                               "status": "OK", "zip_filename": feed.filename}},
                                     upsert=True)
                log.info("Extracted geopackage for type: %s" % doc_type)
    except Exception as e:
        log.error(str(e))
        db.source.update_one({"type": doc_type}, {
                             "$set": {"status": "Failed extracting gpkg"}}, upsert=True)
        return
