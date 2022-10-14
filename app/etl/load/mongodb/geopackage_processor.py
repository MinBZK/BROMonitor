import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, joinedload

from common.config import date_format, logging_format
from etl.configuration.config import registration_types
from etl.load.serializing.get_serializer import get_serializer
from etl.load.serializing.base_schemas.common_schema import Common_Schema
from etl.transform.transform_common import transform_common
from etl.transform.transform_specific import transformer_mapping


class GeopackageProcessor:
    def __init__(self, db, doc_type):
        logging.basicConfig(
            level=os.environ.get("LOGLEVEL", "INFO"),
            format=logging_format,
            datefmt=date_format,
        )
        self.log = logging.getLogger(__name__)
        self.db = db
        self.doc_type = doc_type
        self.unzip_location = os.environ.get("unzipLocation", "/mnt/brodata/")
        self.i18n = {}

    def process(self):
        type_name = self.doc_type.type_name
        self.log.info(f"Start with load process for {type_name}")
        source = self.db.source.find_one({"type": type_name})
        self.log.info(f"{source['last_loaded']} , {source['updated']}")
        # Break if we have loaded already
        if source["last_loaded"] > source["updated"]:
            self.log.info("No new geopackage for: %s" % (type_name))
            self.log.info(
                f"Feed update {source['updated']} < last_loaded {source['last_loaded']}."
            )
            return
        else:
            # Start by clearing the temp collections (safety precaution)
            self.__clear_temp_collections()

            file_name = source["zip_filename"].replace("zip", "gpkg")

            # Change the name till pdok name zip and geopackage the same
            if type_name == "bhr-gt":
                file_name = "brobhrgtvolledigeset.gpkg"

            # Create database engine from the specified geopackage file
            engine = create_engine("sqlite:///" + self.unzip_location + file_name)

            # Reflect the desired database tables
            metadata = MetaData()

            # Relevant DB tables 'usually' start with their prefix, unless the type is sfr (for now)
            if type_name not in ["sfr", "gmn", "bhr-p", "bhr-gt"]:
                metadata.reflect(
                    engine,
                    only=lambda name, _: name.startswith(type_name.replace("-", "")),
                )
            else:
                metadata.reflect(engine)

            Base = automap_base(metadata=metadata)
            Base.prepare()

            # Create database session
            Session = sessionmaker(bind=engine)
            session = Session()

            # Get the python classes reflected from the database
            classes = Base.classes

            # Serialize and load the registration objects
            common_schema = Common_Schema()
            specific_schema = get_serializer(type_name, classes)

            specific_transformer = None

            # Load the transformer for the specifics
            if type_name in transformer_mapping.keys():
                specific_transformer = transformer_mapping[type_name]

            lastPK = i = 0
            c = classes[self.doc_type.main_table]
            pk_col = self.doc_type.pk_col
            pk = getattr(c, pk_col)

            while True:
                # Construct iterator step-wise using the reflected classes and collections
                iterator = session.query(c).filter(pk > lastPK).limit(1000)
                for load in self.doc_type.join_tables:
                    opts = joinedload(load.table_name)
                    parent_type = classes[load.table_name[:-11]]
                    children = load.inner_joins
                    while True:
                        if len(children) != 1:
                            break
                        else:
                            child = children[0]
                            opts = opts.joinedload(
                                getattr(parent_type, child.table_name)
                            )
                            children = child.inner_joins
                            parent_type = classes[child.table_name[:-11]]
                    iterator = iterator.options(opts)
                elems = iterator.all()

                if len(elems) == 0:
                    break

                for elem in elems:
                    # Do not consider deregistered objects
                    if self.__check_if_deregistered_elem(elem):
                        continue
                    lastPK = getattr(elem, pk_col)
                    i += 1
                    json_specific = specific_schema.dump(elem)
                    json_common = common_schema.dump(elem)

                    # If a separate location table is defined, add its values to the common document

                    # SKIP LOCATIONS SINCE GEOPACKAGES DONT INCLUDE THEM ANYMORE
                    # if self.doc_type.location_table:
                    #     for crd in ["xOrLon", "yOrLat"]:
                    #         json_common[crd] = json_specific[
                    #             self.doc_type.location_table
                    #         ][0][crd]

                    # If a separate registration history table is defined, add its values to the common document
                    if self.doc_type.registration_history_table:
                        json_common["objectRegistrationTime"] = json_specific[
                            self.doc_type.registration_history_table
                        ][0]["objectRegistrationTime"]

                    # Transform the commons
                    json_common_transformed = transform_common(
                        json_common, self.doc_type.full_name
                    )

                    # Transform the specifics if a transformer is defined for this type
                    if specific_transformer:
                        json_specific = specific_transformer(json_specific)

                    # Write to temporary/buffer collections
                    specific_result = self.db.tempSpecific.insert_one(json_specific)
                    common_result = self.db.tempCommon.insert_one(
                        json_common_transformed
                    )

                    if i % 1000 == 0:
                        self.log.info("Processed %d %s documents..." % (i, type_name))

        # Overwrite the data from temporary/buffer to the final collections
        self.__overwrite_data()

        self.db.source.update_one(
            {"type": type_name},
            {"$set": {"last_loaded": datetime.now(), "status": "OK"}},
            upsert=True,
        )
        self.log.info("Done loading documents for: %s" % (type_name))

    def __check_if_deregistered_elem(self, elem) -> bool:
        return (hasattr(elem, "deregistered") and elem.deregistered == "ja") or (
            hasattr(elem, "registration_history_collection")
            and elem.registration_history_collection[0].deregistered == "ja"
        )

    def __overwrite_data(self):
        self.log.info(f"Overwriting old data with new for {self.doc_type.type_name}")
        self.__overwrite_common()
        self.__overwrite_specific()
        self.log.info(
            f"Done overwriting old data with new for {self.doc_type.type_name}"
        )

    def __overwrite_specific(self):
        target = self.doc_type.mongo_collection
        self.log.info(f"Overwriting specific collection for {target}")
        self.db.tempSpecific.rename(new_name=target, dropTarget=True)
        self.log.info(f"Done overwriting specific collection for {target}")

    def __overwrite_common(self):
        common_type = self.doc_type.full_name
        self.log.info(f"Overwriting common documents for {common_type}")
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
        self.log.info(f"Done overwriting common documents for {common_type}")

    def __clear_temp_collections(self):
        self.db.tempCommon.drop()
        self.db.tempSpecific.drop()
