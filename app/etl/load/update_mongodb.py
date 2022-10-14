from dateutil import parser
import os
import logging
import csv
from pymongo import MongoClient
from common.config import date_format, logging_format
from etl.configuration.config import registration_types, init_registration_types
from etl.load.mongodb.reset_mongo import reset_mongo

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format=logging_format, datefmt=date_format)
log = logging.getLogger(__name__)

mongoUrl = os.environ.get('mongodbUrl')
client = MongoClient(mongoUrl)
db = client.bro
unzip_location = os.environ.get('unzipLocation', '/mnt/brodata/')


def load_geotop():
    mongoUrl = os.environ.get('mongodbUrl')
    client = MongoClient(mongoUrl)
    db = client.bro

    db.geotop.drop()

    with open('configuration/geotop_dump.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                log.info(f'Column names are {",".join(row)}')
                line_count += 1
            else:
                db.geotop.insert_one(
                    {
                        "x": int(row[0]),
                        "y": int(row[1]),
                        "classes": row[2]
                    })
                line_count += 1
    print(f'Inserted {line_count} geotop records.')


def create_geotop_index():
    mongoUrl = os.environ.get('mongodbUrl')
    client = MongoClient(mongoUrl)
    db = client.bro
    db.geotop.create_index([('x', 1), ('y', 1)])


def update_source():
    init_registration_types()
    for reg_type in registration_types:
        doc_type = reg_type.type_name
        if doc_type == 'cpt':
            db.source.update_one({"type": doc_type},
                                 {"$set": {"status": "OK",
                                           "updated":  parser.parse('2021-03-15T00:00:00.000+00:00'),
                                           "last_extracted": parser.parse('2021-01-01T00:00:00.000+00:00'),
                                           "last_loaded": parser.parse('2021-01-01T00:00:00.000+00:00'),
                                           "zip_filename": "brocptvolledigeset.zip"}},
                                 upsert=True)
        if doc_type == 'bhr':
            db.source.update_one({"type": doc_type},
                                 {"$set": {"status": "OK",
                                           "updated":  parser.parse('2021-03-15T00:00:00.000+00:00'),
                                           "last_extracted": parser.parse('2021-01-01T00:00:00.000+00:00'),
                                           "zip_filename": "brobhrpvolledigeset.zip",
                                           "last_loaded": parser.parse('2021-01-01T00:00:00.000+00:00')}},
                                 upsert=True)
        if doc_type == 'gmw':
            db.source.update_one({"type": doc_type},
                                 {"$set": {"status": "OK",
                                           "updated":  parser.parse('2021-03-15T00:00:00.000+00:00'),
                                           "last_extracted": parser.parse('2021-01-01T00:00:00.000+00:00'),
                                           "zip_filename": "brogmwvolledigeset.zip",
                                           "last_loaded": parser.parse('2021-01-01T00:00:00.000+00:00')}},
                                 upsert=True)
        if doc_type == 'sfr':
            db.source.update_one({"type": doc_type},
                                 {"$set": {"status": "OK",
                                           "updated":  parser.parse('2021-03-15T00:00:00.000+00:00'),
                                           "last_extracted": parser.parse('2021-01-01T00:00:00.000+00:00'),
                                           "zip_filename": "brosfrvolledigeset.zip",
                                           "last_loaded": parser.parse('2021-01-01T00:00:00.000+00:00')}},
                                 upsert=True)
        if doc_type == 'bhr-gt':
            db.source.update_one({"type": doc_type},
                                 {"$set": {"status": "OK",
                                           "updated":  parser.parse('2021-03-15T00:00:00.000+00:00'),
                                           "last_extracted": parser.parse('2021-01-01T00:00:00.000+00:00'),
                                           "zip_filename": "brobhrgt.zip",
                                           "last_loaded": parser.parse('2021-01-01T00:00:00.000+00:00')}},
                                 upsert=True)


# reset_mongo()
# load_geotop()
create_geotop_index()
