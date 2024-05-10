import logging
import os
import csv
from pymongo import MongoClient
import pandas as pd

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
        df = pd.read_csv(csv_path, encoding='ISO-8859-1', delimiter=';', dtype={'KVK': str})

        df['KVK'] = df['KVK'].astype(str)
        df['KVK'] = df['KVK'].apply(lambda x: '0' + x if len(x) == 7 and x != '2442829' else x)
        
        log.info(f'Column names are {",".join(df.columns)}')
        for index, row in df.iterrows(): 
            if "Gemeente" in row.iloc[2]:
                type = "Gemeente"
            elif "Provincie" in row.iloc[2]:
                type = "Provincie"
            elif "Water" in row.iloc[2]:
                type = "Waterschap"
            else:
                type = "Overig"
            db.bronhouder.insert_one(
                {
                    "kvk": row.iloc[4],
                    "naam": row.iloc[0],
                    "type": type,
                    "identifier": "" if pd.isna(row.iloc[5]) else row.iloc[5],
                    "isBronhouder": row.iloc[4] in bronhouders_set
                })
        log.info(f'Loaded {index} bronhouders to mongoDb.')
