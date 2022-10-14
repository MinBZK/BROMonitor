from backend.utils.documentTypes import document_type_registry
from backend.queries.metadata import get_source_model_by_types
from backend.models.bronhouder import Bronhouder
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from backend.models.aggregate import (
    Top20Aggregate,
    QualityRegimeAggregate,
    CountAggregate,
    PerBronhouderCountAggregate,
    BronhouderAndType,
    DataModel,
    SourceModel,
    BronhoudersPerMonth,
)


async def get_bronhouders(conn: AsyncIOMotorClient):
    data: List[Bronhouder] = []
    cursorBronhouders = conn.bro.bronhouder.find({"isBronhouder": True})
    async for row in cursorBronhouders:
        data.append(
            Bronhouder(name=row["naam"], kvk=row["kvk"], identifier=row["identifier"])
        )
    return data


async def get_bronhouders_kvk_dic(
    conn: AsyncIOMotorClient, bh_filter="", withIdentifier=False
):
    if bh_filter:
        cursorBronhouders = conn.bro.bronhouder.find(bh_filter)
    else:
        cursorBronhouders = conn.bro.bronhouder.find()
    bronhoudersDict = {}
    async for row in cursorBronhouders:
        if withIdentifier:
            bronhoudersDict[row["kvk"]] = [row["naam"], row["identifier"]]
        else:
            bronhoudersDict[row["kvk"]] = row["naam"]
    return bronhoudersDict


async def get_brondocumenten_count_by_bronhouder(
    bronhoudertype: str, gldstatus: str, conn: AsyncIOMotorClient, only_bronhouders=True
):
    data: List[PerBronhouderCountAggregate] = []

    # Load the bronhouders collection locally in memory
    if bronhoudertype and only_bronhouders:
        bh_filter = {"type": bronhoudertype, "isBronhouder": True}
    elif only_bronhouders:
        bh_filter = {"isBronhouder": True}
    elif bronhoudertype:
        bh_filter = {"type": bronhoudertype}
    else:
        bh_filter = {}

    bronhoudersDict = await get_bronhouders_kvk_dic(conn, bh_filter, True)

    # add the bronhouders with documents
    cursorDocumentCounts = conn.bro.documentCountsByBronhouder.find()
    async for row in cursorDocumentCounts:
        if row["_id"]["kvk"] in bronhoudersDict:
            kvk = row["_id"]["kvk"]
            data.append(
                PerBronhouderCountAggregate(
                    key=BronhouderAndType(
                        kvk=kvk,
                        naam=bronhoudersDict[kvk][0],
                        identifier=bronhoudersDict[kvk][1],
                        type=row["_id"]["type"],
                    ),
                    count=row["count"],
                )
            )

    # check if gld should be added and glds with status aangevuld
    if gldstatus:
        # add the bronhouders with glds
        cursorDocumentCounts = conn.bro.gldsCountsByBronhouder.find()
        async for row in cursorDocumentCounts:
            if (
                row["_id"]["kvk"] in bronhoudersDict
                and row["_id"]["status"] == "aangevuld"
            ):
                kvk = row["_id"]["kvk"]
                data.append(
                    PerBronhouderCountAggregate(
                        key=BronhouderAndType(
                            kvk=kvk,
                            naam=bronhoudersDict[kvk][0],
                            identifier=bronhoudersDict[kvk][1],
                            type="Grondwaterstandonderzoek_aangevuld",
                            status=row["_id"]["status"],
                        ),
                        count=row["count"],
                    )
                )

    # add the bronhouders without documents
    for kvk, bh in bronhoudersDict.items():
        if not bh[0] in map(lambda x: x.key.naam, data):
            data.append(
                PerBronhouderCountAggregate(
                    key=BronhouderAndType(
                        kvk=kvk, naam=bh[0], identifier=bh[1], type=""
                    ),
                    count=0,
                )
            )

    source: SourceModel = await get_source_model_by_types(
        conn, "pdok", document_type_registry.get_short_names()
    )
    return DataModel(data=data, sources=[source])


async def get_quality_regimes_by_bronhouder(
    bronhoudertype: str, conn: AsyncIOMotorClient
):
    data: List[QualityRegimeAggregate] = []

    bronhoudersDict = await get_bronhouders_kvk_dic(
        conn, {"type": bronhoudertype}, True
    )

    pipeline = [
        {"$sort": {"common.deliveryAccountableParty": 1}},
        {
            "$group": {
                "_id": {
                    "kvk": "$common.deliveryAccountableParty",
                    "quality_regime": "$common.qualityRegime",
                },
                "count": {"$sum": 1},
            }
        },
        {
            "$group": {
                "_id": "$_id.kvk",
                "quality_regimes": {
                    "$push": {
                        "quality_regime": "$_id.quality_regime",
                        "count": "$count",
                    }
                },
            }
        },
    ]
    # Create results for the bronhouders with registered documents
    async for row in conn.bro.common.aggregate(pipeline):
        if row["_id"] in bronhoudersDict:
            kvk = row["_id"]
            quality_regimes: List[CountAggregate] = []
            for regime in row["quality_regimes"]:
                quality_regimes.append(
                    CountAggregate(key=regime["quality_regime"], count=regime["count"])
                )
            quality_regimes.sort(key=lambda x: x.key)
            data.append(
                QualityRegimeAggregate(
                    bronhouder=bronhoudersDict[kvk][0],
                    identifier=bronhoudersDict[kvk][1],
                    quality_regimes=quality_regimes,
                )
            )

    # Create results for the bronhouders without documents
    for kvk, bh in bronhoudersDict.items():
        if bh[0] not in map(lambda x: x.bronhouder, data):
            data.append(
                QualityRegimeAggregate(
                    bronhouder=bh[0], identifier=bh[1], quality_regimes=[]
                )
            )

    source: SourceModel = await get_source_model_by_types(
        conn, "pdok", document_type_registry.get_short_names()
    )
    return DataModel(data=data, sources=[source])


async def get_top20(conn: AsyncIOMotorClient, object_type: str):
    data: List[CountAggregate] = []

    bronhoudersDict = await get_bronhouders_kvk_dic(conn)

    pipeline = [
        {"$group": {"_id": "$common.deliveryAccountableParty", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20},
    ]

    # If a type is specified, prepend a filter on that type to the pipeline
    if object_type:
        pipeline = [{"$match": {"common.type": {"$eq": object_type}}}] + pipeline
        source_types = [document_type_registry.get_short_by_dbname(object_type)]
    else:
        source_types = document_type_registry.get_short_names()

    async for row in conn.bro.common.aggregate(pipeline):
        kvk = row["_id"]
        data.append(CountAggregate(key=bronhoudersDict[kvk], count=row["count"]))

    source: SourceModel = await get_source_model_by_types(conn, "pdok", source_types)
    return DataModel(data=data, sources=[source])


async def get_top20_since_date(conn: AsyncIOMotorClient, start_date):
    data: List[Top20Aggregate] = []

    bronhoudersDict = await get_bronhouders_kvk_dic(conn)

    pipeline = [
        {
            "$project": {
                "date": {
                    "$dateFromString": {"dateString": "$common.objectRegistrationTime"}
                },
                "common.type": 1,
                "common.qualityRegime": 1,
                "common.deliveryAccountableParty": 1,
            }
        },
        {"$match": {"date": {"$gt": start_date}}},
        {
            "$group": {
                "_id": {
                    "kvk": "$common.deliveryAccountableParty",
                    "type": "$common.type",
                },
                "count": {"$sum": 1},
                "imbro_count": {
                    "$sum": {
                        "$cond": {
                            "if": {"$eq": ["$common.qualityRegime", "IMBRO"]},
                            "then": 1,
                            "else": 0,
                        }
                    }
                },
                "imbroa_count": {
                    "$sum": {
                        "$cond": {
                            "if": {"$eq": ["$common.qualityRegime", "IMBRO/A"]},
                            "then": 1,
                            "else": 0,
                        }
                    }
                },
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 5000},
    ]
    source_types = document_type_registry.get_short_names()

    async for row in conn.bro.common.aggregate(pipeline):
        kvk = row["_id"]["kvk"]
        data.append(
            Top20Aggregate(
                bronhouder=bronhoudersDict[kvk]
                if kvk in bronhoudersDict.keys()
                else kvk,
                object_type=row["_id"]["type"],
                imbro_count=row["imbro_count"],
                imbroa_count=row["imbroa_count"],
            )
        )

    source: SourceModel = await get_source_model_by_types(conn, "pdok", source_types)
    return DataModel(data=data, sources=[source])


async def get_bronhouders_over_time(conn: AsyncIOMotorClient):
    data: List[BronhoudersPerMonth] = []

    bronhoudersDict = await get_bronhouders_kvk_dic(conn, withIdentifier=True)

    pipeline = [
        {
            "$project": {
                "date": {
                    "$dateFromString": {"dateString": "$common.objectRegistrationTime"}
                },
                "common.type": 1,
                "common.deliveryAccountableParty": 1,
            }
        },
        {
            "$group": {
                "_id": {
                    "type": "$common.type",
                    "kvk": "$common.deliveryAccountableParty",
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                },
                "count": {"$sum": 1},
            }
        },
    ]

    async for row in conn.bro.common.aggregate(pipeline):
        kvk = row["_id"]["kvk"]
        data.append(
            BronhoudersPerMonth(
                kvk=kvk,
                naam=bronhoudersDict[kvk][0],
                identifier=bronhoudersDict[kvk][1],
                monthyear=(row["_id"]["month"], row["_id"]["year"]),
                object_type=row["_id"]["type"],
                count=row["count"],
            )
        )

    source: SourceModel = await get_source_model_by_types(
        conn, "pdok", document_type_registry.get_short_names()
    )
    return DataModel(data=data, sources=[source])
