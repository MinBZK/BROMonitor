import csv
from datetime import datetime
import json
import os
import logging
import time
from pymongo import MongoClient
import functools
import requests

from common.config import date_format, logging_format
from etl.load.mongodb.mongo_helpers import initiliaze_source_document


logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format=logging_format, datefmt=date_format
)
logger = logging.getLogger(__name__)


class GLDExtractor:
    """
    Extracts GLD XML files using the open bro api.
    """

    def __init__(self):
        mongoUrl = os.environ.get("mongodbUrl")
        client = MongoClient(mongoUrl)
        self.db = client.bro
        self.doc_type = "gld"
        self.API_URL = "https://publiek.broservices.nl/gm/gld/v1/"
        self.extract_path = os.environ.get("downloadLocation", "/mnt/brodata/")
        self.bronhouder_kvks = []
        self.bronhouder_broids = {}
        initiliaze_source_document(self.db, self.doc_type)            

    def __update_metadata(self):
        """
        Updates metadata of the ETL proces in mongodb.
        """
        self.db.source.update_one(
            {"type": self.doc_type},
            {"$set": {"last_extracted": datetime.now()}},
            upsert=True,
        )

    def __get_bronhouder_kvks(self):
        """
        Fetches known bronhouder kvks from mongodb and adds them to memory.
        """
        cursorBronhouders = self.db.bronhouder.find({"isBronhouder": True})
        for row in cursorBronhouders:
            self.bronhouder_kvks.append(row["kvk"])

    def __get_bronhouder_broids(self):
        """
        Using the public BRO API fetch all GLD BROIDS for every bronhouder kvk and add them to memory.
        """
        with requests.Session() as session:
            for kvk in self.bronhouder_kvks:
                response = session.get(
                    f"{self.API_URL}bro-ids", params={"bronhouder": kvk}
                )
                if response.status_code == 200:
                    content = json.loads(response.content)
                    bro_ids = content.get("broIds", [])
                    if bro_ids:
                        self.bronhouder_broids[kvk] = bro_ids
                else:
                    logger.warning("Non 200 return code")

    def __extract_xml_file(self, session, bro_id, max_tries=3):
        """
        Attempts to extract a single XML file n times. If after n times there is still no success, raise exception.

        Returns: The succesful response if any
        """
        last_exception = None
        today = datetime.today().strftime("%Y-%m-%d")
        for i in range(max_tries):
            if i > 0:
                time.sleep(1)
            try:
                response = session.get(
                    f"{self.API_URL}objects/{bro_id}",
                    params={"observationPeriodBeginDate": today},
                )
                return response
            except Exception as e:
                logger.error(
                    f"An exception occured downloading {bro_id}: {e}. Try {i + 1} of {max_tries}."
                )
                last_exception = e
        if last_exception:
            raise last_exception
        raise RuntimeError

    def __extract_xml_files(self):
        """
        Using the public BRO API extract all XML GLD files for known BROIDS.
        """
        with requests.Session() as session:
            all_bro_ids = functools.reduce(lambda x, y: x+y, self.bronhouder_broids.values())
            for bro_id_index, bro_id in enumerate(all_bro_ids):
                response = self.__extract_xml_file(session=session, bro_id=bro_id)
                if response.status_code == 200:
                    content = response.content.decode("utf-8")
                    filename = os.path.join(
                        self.extract_path, "gld", f"{bro_id}.xml"
                    )
                    if not os.path.exists(os.path.dirname(filename)):
                        os.makedirs(os.path.dirname(filename))
                    with open(filename, "w") as f:
                        f.write(content)
                if (bro_id_index+1) % 50 == 0:
                    logger.info(f"Handled {bro_id_index+1}/{len(all_bro_ids)} broids")

    def extract(self):
        """
        Extracts GLD XML files using the Open BRO API and writes them to disk.
        """
        try:
            logger.info("Getting bronhouder kvks.")
            self.__get_bronhouder_kvks()
            logger.info("Getting bronhouder broids.")
            self.__get_bronhouder_broids()
            logger.info("Extracting XML files per bronhouder.")
            self.__extract_xml_files()
            logger.info("Updating metadata.")
            self.__update_metadata()
        except Exception as e:
            logger.error(str(e))
            self.db.source.update_one(
                {"type": self.doc_type},
                {"$set": {"status": "Failed extracting xmls"}},
                upsert=True,
            )
