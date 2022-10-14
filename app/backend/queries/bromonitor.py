from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from backend.models.aggregate import SourceModel, BromonitorModel, BromonitorModelRecent
from backend.models.dates import DatesModel
from backend.queries.metadata import get_source_model_by_types
from backend.utils.documentTypes import document_type_registry
from backend.utils.getStaticConent import get_static_html


async def get_bromonitor_by_date(conn: AsyncIOMotorClient, date: datetime):
    cursorBromonitor = await conn.bro.bromonitor.find_one({"date": date})
    data: BromonitorModel = BromonitorModel(
        date=cursorBromonitor["date"].strftime("%d-%m-%Y"),
        html=cursorBromonitor["html"],
    )
    return data


async def get_bromonitor_embedded(conn: AsyncIOMotorClient):
    dates = await get_bromonitor_dates(conn)
    cursor = await conn.bro.bromonitor.find_one(
        {"most_recent": False, "date": dates.dates[0]}
    )
    data: BromonitorModel = BromonitorModel(
        date=cursor["date"].strftime("%d-%m-%Y"), html=cursor["html"]
    )
    return data


async def get_bromonitor_recent(conn: AsyncIOMotorClient):
    cursor = await conn.bro.bromonitor.find_one({"most_recent": True})
    static_content = get_static_html(cursor["html"])
    static_data = cursor["static_data"] if "static_data" in cursor else {}
    data: BromonitorModelRecent = BromonitorModelRecent(
        date=cursor["date"].strftime("%d-%m-%Y"), html=cursor["html"], static=static_content, static_data=static_data
    )
    return data


async def get_bromonitor_dates(conn: AsyncIOMotorClient):
    dates = []
    pipeline = [
        {
            "$group": {
                "_id": "$date",
            }
        },
        {"$sort": {"_id": -1}},
    ]
    async for row in conn.bro.bromonitor.aggregate(pipeline):
        dates.append(row["_id"])
    return DatesModel(dates=dates)


async def get_bromonitor_timestamp(conn: AsyncIOMotorClient):
    source: SourceModel = await get_source_model_by_types(
        conn, "pdok", document_type_registry.get_short_names()
    )
    return source
