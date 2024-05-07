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
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                log.info(f'Column names are {",".join(row)}')
                line_count += 1
            else:
                if "Gemeente" in row[2]:
                    type = "Gemeente"
                    identifier = "GM00"
                elif "Provincie" in row[2]:
                    type = "Provincie"
                    identifier = "PV00"
                elif "Water" in row[2]:
                    type = "Waterschap"
                    identifier = "WS00"
                else:
                    type = "Overig"
                    identifier = ""
                db.bronhouder.insert_one(
                    {
                        "kvk": row[4],
                        "naam": row[0],
                        "type": type,
                        "identifier": identifier,
                        "isBronhouder": row[4] in bronhouders_set
                    })
                line_count += 1
        log.info(f'Loaded {line_count} bronhouders to mongoDb.')
