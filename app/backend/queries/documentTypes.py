from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from backend.models.aggregate import (
    CountAggregate,
    PerBronhouderCountAggregate,
    BronhouderAndType,
    DataModel,
    SourceModel,
    ObjectTypeRegimeAggregate,
)
from backend.queries.metadata import get_source_model_by_types
from backend.utils.documentTypes import document_type_registry
from backend.queries.bronhouders import get_bronhouders_kvk_dic
import datetime


async def get_document_types(conn: AsyncIOMotorClient):
    data: List[CountAggregate] = []
    pipeline = [
        {"$group": {"_id": "$common.type", "count": {"$sum": 1}}},
        {"$sort": {"count": 1}},
    ]

    async for row in conn.bro.common.aggregate(pipeline):
        data.append(CountAggregate(key=row["_id"], count=row["count"]))

    source: SourceModel = await get_source_model_by_types(
        conn, "pdok", document_type_registry.get_short_names()
    )
    return DataModel(data=data, sources=[source])


async def get_document_delta(conn: AsyncIOMotorClient, start_date):
    start_date = datetime.datetime(1900, 1, 1) if not start_date else start_date
    data: List[ObjectTypeRegimeAggregate] = []
    pipeline = [
        {
            "$project": {
                "date": {
                    "$dateFromString": {"dateString": "$common.objectRegistrationTime"}
                },
                "common.type": 1,
                "common.qualityRegime": 1,
            }
        },
        {"$match": {"date": {"$gt": start_date}}},
        {
            "$group": {
                "_id": {
                    "type": "$common.type",
                    "quality_regime": "$common.qualityRegime",
                },
                "count": {"$sum": 1},
            }
        },
    ]

    async for row in conn.bro.common.aggregate(pipeline):
        data.append(
            ObjectTypeRegimeAggregate(
                object_type=row["_id"]["type"],
                quality_regime=row["_id"]["quality_regime"],
                count=row["count"],
            )
        )

    source: SourceModel = await get_source_model_by_types(
        conn, "pdok", document_type_registry.get_short_names()
    )
    return DataModel(data=data, sources=[source])


async def get_documents_over_time(conn: AsyncIOMotorClient, object_type: str):
    data: List[CountAggregate] = []
    pipeline = [
        {"$match": {"common.type": {"$eq": object_type}}},
        {
            "$group": {
                "_id": {
                    "$year": {
                        "$dateFromString": {
                            "dateString": "$common.objectRegistrationTime"
                        }
                    }
                },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    async for row in conn.bro.common.aggregate(pipeline):
        data.append(CountAggregate(key=row["_id"], count=row["count"]))

    source: SourceModel = await get_source_model_by_types(
        conn, "pdok", [document_type_registry.get_short_by_dbname(object_type)]
    )
    return DataModel(data=data, sources=[source])


async def get_glds_updated(conn: AsyncIOMotorClient, start_date):
    start_date = datetime.datetime(1900, 1, 1) if not start_date else start_date
    data: List[PerBronhouderCountAggregate] = []

    bronhoudersDict = await get_bronhouders_kvk_dic(conn)

    pipeline = [
        {
            "$project": {
                "date": {"$dateFromString": {"dateString": "$researchLastDate"}},
                "deliveryAccountableParty": 1,
            }
        },
        {"$match": {"date": {"$gt": start_date}}},
        {"$group": {"_id": {"kvk": "$deliveryAccountableParty"}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]

    async for row in conn.bro.specificGLD.aggregate(pipeline):
        kvk = row["_id"]["kvk"]
        data.append(
            PerBronhouderCountAggregate(
                key=BronhouderAndType(kvk=kvk, naam=bronhoudersDict[kvk]),
                count=row["count"],
            )
        )

    source: SourceModel = await get_source_model_by_types(conn, "pdok", ["gld"])
    return DataModel(data=data, sources=[source])


async def get_glds_start_update_count(conn: AsyncIOMotorClient):
    data: List[PerBronhouderCountAggregate] = []

    bronhoudersDict = await get_bronhouders_kvk_dic(conn)

    cursorDocumentCounts = conn.bro.gldsCountsByBronhouder.find()
    async for row in cursorDocumentCounts:
        data.append(
            PerBronhouderCountAggregate(
                key=BronhouderAndType(
                    kvk=row["_id"]["kvk"],
                    naam=bronhoudersDict[row["_id"]["kvk"]],
                    status=row["_id"]["status"],
                ),
                count=row["count"],
            )
        )

    source: SourceModel = await get_source_model_by_types(conn, "pdok", ["gld"])
    return DataModel(data=data, sources=[source])
