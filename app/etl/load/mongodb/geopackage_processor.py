import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError

from common.config import date_format, logging_format
from etl.load.serializing.get_serializer import get_serializer
from etl.load.serializing.base_schemas.common_schema import Common_Schema
from etl.transform.transform_common import transform_common
from etl.transform.transform_specific import transformer_mapping
from gmw_gmn_gld_processing import adjust_geopackage

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
        self.type_name = self.doc_type.type_name
        self.file_name = self.get_file_name()


    def get_file_name(self):
        source = self.db.source.find_one({"type": self.type_name})

        file_name = source["zip_filename"]

        # Change the name till pdok name zip and geopackage the same
        if self.type_name == "bhr-gt":
            file_name = "brobhrgtvolledigeset.gpkg"
        
        if "zip" in file_name:
            file_name = file_name.replace("zip", "gpkg")
        
        return file_name

    
    def check_geopackage_exists(self):
        file_path = os.path.join(self.unzip_location, self.file_name)
        
        # Check if the GeoPackage exists
        if not os.path.exists(file_path):
            return False
        return True


    def check_geopackage_integrity(self):
        engine = create_engine("sqlite:///" + self.unzip_location + self.file_name)

        try:
            with engine.connect() as connection:
                # Execute PRAGMA integrity_check
                integrity_check = connection.execute(text("PRAGMA integrity_check;")).fetchall()
                
                if integrity_check[0][0] != "ok":
                    self.log.error(f"GeoPackage {self.file_name} integrity check failed: {integrity_check}")
                    return False
   
                self.log.info(f"GeoPackage {self.file_name} integrity check passed.")
                return True
            
        except Exception as e:
            return self.log.error(f"An error occurred while checking integrity: {e}")
        finally:
            engine.dispose()


    def process(self):
        self.log.info(f"Start with load process for {self.type_name}")
        
        source = self.db.source.find_one({"type": self.type_name})

        last_loaded_datetime = source["last_loaded"]
        updated_datetime = source["updated"]

        self.log.info(f"{last_loaded_datetime} , {updated_datetime}")
        # Break if we have loaded already
        if last_loaded_datetime > updated_datetime or not self.check_geopackage_exists():
            self.log.info("No new Geopackage for %s" % (self.type_name))
            self.log.info(
                f"Feed update {updated_datetime} < last_loaded {last_loaded_datetime}."
            )
            return


        else:
            # Start by clearing the temp collections (safety precaution)
            self.__clear_temp_collections()

            if not self.check_geopackage_integrity():
                self.log.error("GeoPackage integrity check failed. Aborting processing..")
                return 

            # Create database engine from the specified geopackage file
            engine = create_engine("sqlite:///" + self.unzip_location + self.file_name)

            # Reflect the desired database tables
            metadata = MetaData()

            try:
                metadata.reflect(engine)
                
                if self.type_name in ["gmn", "gmw", "gld"]:
                    adjust_geopackage(metadata, engine)

                Base = automap_base(metadata=metadata)
                Base.prepare()

                # Create database session
                Session = sessionmaker(bind=engine)
                with Session() as session:

                    # Get the python classes reflected from the database
                    classes = Base.classes
                    # Serialize and load the registration objects
                    common_schema = Common_Schema()
                    specific_schema = get_serializer(self.type_name, classes)

                    specific_transformer = None

                    # Load the transformer for the specifics
                    if self.type_name in transformer_mapping.keys():
                        specific_transformer = transformer_mapping[self.type_name]

                    lastPK = i = 0
                    c = classes[self.doc_type.main_table]
                    pk_col = self.doc_type.pk_col
                    pk = getattr(c, pk_col)

                    while True:
                        # Construct iterator step-wise using the reflected classes and collections
                        iterator = session.query(c).filter(pk > lastPK).limit(1000)
                        for load in self.doc_type.join_tables:
                            if load.table_name[:-11] not in classes:
                                self.log.error(f"Table '{load.table_name[:-11]}' does not exist in the reflected classes.")
                            
                            opts = joinedload(getattr(c, load.table_name))
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
                            self.db.tempSpecific.insert_one(json_specific)
                            self.db.tempCommon.insert_one(
                                json_common_transformed
                            )

                            if i % 1000 == 0:
                                self.log.info("Processed %d %s documents..." % (i, self.type_name))
                
            except SQLAlchemyError as e:
                self.log.error(f"Database error occurred: {e}")   
            finally:
                engine.dispose()

        # Overwrite the data from temporary/buffer to the final collections
        self.__overwrite_data()

        self.db.source.update_one(
            {"type": self.type_name},
            {"$set": {"last_loaded": datetime.now(), "status": "OK"}},
            upsert=True,
        )
        self.log.info("Done loading documents for: %s" % (self.type_name))

    def __check_if_deregistered_elem(self, elem) -> bool:
        return (hasattr(elem, "deregistered") and elem.deregistered == "ja") or (
            hasattr(elem, "registration_history_collection")
            and elem.registration_history_collection[0].deregistered == "ja"
        )

    def __overwrite_data(self):
        self.log.info(f"Overwriting old data with new for {self.type_name}")
        self.__overwrite_common()
        self.__overwrite_specific()
        self.log.info(
            f"Done overwriting old data with new for {self.type_name}"
        )

    def __overwrite_specific(self):
        target = self.doc_type.mongo_collection
        self.log.info(f"Overwriting specific collection for {target}")
        self.db.tempSpecific.rename(new_name=target, dropTarget=True)
        self.log.info(f"Done overwriting specific collection for {target}")

    def __overwrite_common(self):
        common_type = self.doc_type.full_name
        self.log.info(f"Overwriting common documents for {common_type}")
        self.db.common.delete_many({"common.type": common_type})
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
            ],
            allowDiskUse=True
        )
        
        query = { 'common.qualityRegime': None }
        # Delete rows with NaN values
        self.db.common.delete_many(query)

        self.db.tempCommon.drop()
        self.log.info(f"Done overwriting common documents for {common_type}")

    def __clear_temp_collections(self):
        self.db.tempCommon.drop()
        self.db.tempSpecific.drop()
