from motor.motor_asyncio import AsyncIOMotorClient
from typing import List

from backend.models.dates import DatetimeModel
from backend.models.source import SourceModel, SourceTypeModel
from backend.utils.documentTypes import document_type_registry


async def get_document_types(conn: AsyncIOMotorClient):
    return document_type_registry.get_types()


# Gets the source model of the specified type e.g. "gmw"
# from the specified source name e.g. "pdok"


async def __get_sourcetype_model(conn: AsyncIOMotorClient, name: str, type: str):
    document = await conn.bro.source.find_one({"type": type, "name": name})
    source_type_model = (
        SourceTypeModel(type=document["type"].upper(), updated=document["updated"])
        if document
        else SourceTypeModel(type=type, updated=None)
    )
    return source_type_model


# Gets the source model of the newest type in the list of types given as
#  a parameter of the source with the name given as a parameter
# e.g. name="pdok" types=["cpt", "gmw"]


async def get_source_model_by_types(
    conn: AsyncIOMotorClient, name: str, types: List[str]
):
    source_type_models = []
    for t in types:
        source_type_models.append(await __get_sourcetype_model(conn, name, t.lower()))
    result = SourceModel(name=name, types=source_type_models)
    return result


# TODO: ifNull check is not needed after BHR-P is converted to geopackage format
async def get_youngest_object(conn: AsyncIOMotorClient):
    pipeline = [
        {
            "$project": {
                "date": {
                    "$dateFromString": {
                        "dateString": {
                            "$ifNull": [
                                "$common.objectRegistrationTime",
                                "$common.registrationHistory.objectRegistrationTime",
                            ]
                        }
                    }
                }
            }
        },
        {"$sort": {"date": -1}},
        {"$limit": 1},
    ]
    async for row in conn.bro.common.aggregate(pipeline):
        youngest_object = row["date"]
    return DatetimeModel(date=youngest_object)
