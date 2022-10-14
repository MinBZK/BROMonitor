import logging
import os
import csv
from pymongo import MongoClient

from etl.extract.scrape_bronhouders import BronhouderScraper
from common.config import date_format, logging_format


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format=logging_format, datefmt=date_format)
log = logging.getLogger(__name__)


def index_bronhouders():
    scraper = BronhouderScraper()
    scraper.scrape()
    bronhouders_set = scraper.read_pickle()

    mongoUrl = os.environ.get('mongodbUrl')
    client = MongoClient(mongoUrl)
    db = client.bro
    csv_path = os.path.join(os.path.dirname(__file__), '../configuration/bronhouders.csv')
    with open(csv_path, encoding="UTF8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                log.info(f'Column names are {",".join(row)}')
                line_count += 1
            else:
                db.bronhouder.insert_one(
                    {
                        "kvk": row[1],
                        "naam": row[2],
                        "type": row[3],
                        "identifier": row[4],
                        "isBronhouder": row[1] in bronhouders_set
                    })
                line_count += 1
        log.info(f'Loaded {line_count} bronhouders to mongoDb.')
