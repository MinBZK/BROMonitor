from os import listdir
import os
from os.path import isfile, join
from pymongo.mongo_client import MongoClient
import xmltodict
from datetime import datetime
import logging
from pymongo import MongoClient
from common.config import date_format, logging_format

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format=logging_format, datefmt=date_format
)
logger = logging.getLogger(__name__)


class GLDLoader:
    def __init__(self):
        mongoUrl = os.environ.get("mongodbUrl")
        client = MongoClient(mongoUrl)
        self.db = client.bro
        download_location = os.environ.get("downloadLocation", "/mnt/brodata/")
        self.extract_path = os.path.join(download_location, "gld")
        self.namespaces = {"ns11": None, "brocom": None, "gldcommon": None}
        self.full_name = "Grondwaterstandonderzoek"
        self.type_name = "gld"
        self.mongo_collection = "specificGLD"

    def __overwrite_data(self):
        """
        Overwrites the temporary collections to the main collections.
        """
        logger.info(f"Overwriting old data with new for {self.type_name}")
        self.__overwrite_common()
        self.__overwrite_specific()
        logger.info(f"Done overwriting old data with new for {self.type_name}")

    def __overwrite_specific(self):
        """
        Overwrites the temporary specific collection to the permanent one.
        """
        target = self.mongo_collection
        logger.info(f"Overwriting specific collection for {target}")
        self.db.tempSpecific.rename(new_name=target, dropTarget=True)
        logger.info(f"Done overwriting specific collection for {target}")

    def __overwrite_common(self):
        """
        Overwrites the temporary common objects into the permanent common.
        """
        common_type = self.full_name
        logger.info(f"Overwriting common documents for {common_type}")
        self.db.common.remove({"common.type": common_type})
        self.db.tempCommon.aggregate(
            [
                {
                    "$merge": {
                        "into": {"db": "bro", "coll": "common"},
                        "on": "_id",
                        "whenMatched": "replace",
                        "whenNotMatched": "insert",
                    }
                }
            ]
        )
        self.db.tempCommon.drop()
        logger.info(f"Done overwriting common documents for {common_type}")

    def __clear_temp_collections(self):
        """
        Clears temp collections if they still exist.
        """
        self.db.tempCommon.drop()
        self.db.tempSpecific.drop()

    def __check_is_deregistered(self, gld_in: dict) -> bool:
        """
        Checks if a GLD object has been deregistered or not.
        """
        bro_do = gld_in["dispatchDataResponse"]["dispatchDocument"].get("BRO_DO", False)
        if not bro_do:
            return False
        else:
            return bro_do["deregistered"] == "ja"

    def __transform_common(self, gld_in: dict) -> dict:
        """
        Transforms the GLD object into the object we expect for the common collection in mongodb.
        Selects needed values, omits the rest.
        """
        common = {
            "common": {
                "deliveryAccountableParty": gld_in["deliveryAccountableParty"],
                "objectRegistrationTime": gld_in["registrationHistory"][
                    "objectRegistrationTime"
                ],
                "broId": gld_in["broId"],
                "qualityRegime": gld_in["qualityRegime"],
                "type": "Grondwaterstandonderzoek",
            }
        }
        return common

    def __transform_specific(self, gld_in: dict) -> dict:
        """
        Transforms the GLD object into the object we expect for the specific collection in mongodb.
        Selects needed values, omits the rest.
        """
        specific = {
            "deliveryAccountableParty": gld_in["deliveryAccountableParty"],
            "broId": gld_in["broId"],
            "qualityRegime": gld_in["qualityRegime"],
            "registrationHistory": {
                "objectRegistrationTime": gld_in["registrationHistory"][
                    "objectRegistrationTime"
                ],
                "registrationStatus": gld_in["registrationHistory"][
                    "registrationStatus"
                ]["#text"],
            },
            "groundwaterMonitoringTube": {
                "broId": gld_in["monitoringPoint"]["GroundwaterMonitoringTube"][
                    "broId"
                ],
                "tubeNumber": int(
                    gld_in["monitoringPoint"]["GroundwaterMonitoringTube"]["tubeNumber"]
                ),
            },
        }
        first_date = gld_in.get("researchFirstDate", None)
        if first_date:
            specific["researchFirstDate"] = first_date
        last_date = gld_in.get("researchLastDate", None)
        if last_date:
            specific["researchLastDate"] = last_date
        return specific

    def __proces_single_file(self, xml_file_path: str):
        """
        Transforms and loads a single XML file.
        """
        f = open(join(self.extract_path, xml_file_path), "rb")
        input_file = xmltodict.parse(f, namespaces=self.namespaces)
        if self.__check_is_deregistered(input_file):
            return
        data = input_file["dispatchDataResponse"]["dispatchDocument"]["GLD_O"]
        common = self.__transform_common(data)
        specific = self.__transform_specific(data)
        self.db.tempCommon.insert_one(common)
        self.db.tempSpecific.insert_one(specific)

    def load(self):
        """
        Loads all GLD XML files from disk to mongodb.
        """
        logger.info("Started loading GLD objects.")
        self.__clear_temp_collections()
        xmls = [
            f for f in listdir(self.extract_path) if isfile(join(self.extract_path, f))
        ]
        for xml in xmls:
            self.__proces_single_file(xml)
        self.__overwrite_data()
        self.db.source.update_one(
            {"type": self.type_name},
            {
                "$set": {
                    "last_loaded": datetime.now(),
                    "status": "OK",
                    "updated": datetime.now(),
                }
            },
            upsert=True,
        )
