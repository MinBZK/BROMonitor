from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import List
from backend.models.aggregate import CountAggregate


async def log_page_visit(conn: AsyncIOMotorClient, url: str):
    conn.bro.pageVisits.update_one(
        {'url': url, 'date': datetime.now().strftime('%Y-%m-%d')}, {'$inc': {'visits': 1}}, upsert=True)


async def get_page_visits(conn: AsyncIOMotorClient, days=7):
    data: List[CountAggregate] = []
    pipeline = [
        {
            "$project": {
                "date": {
                    "$dateFromString": {
                        "dateString": "$date"
                    }
                },
                "url": 1,
                "visits": 1,
            }
        },
        {
            "$match": {"date": {"$gte": datetime.now() - timedelta(days=days)}}
        },
        {
            "$group": {
                "_id": "$url",
                "count": {"$sum": "$visits"}}
        },
        {
            "$sort": {"count": -1, "_id": 1}
        }
    ]
    async for row in conn.bro.pageVisits.aggregate(pipeline):
        data.append(CountAggregate(key=row["_id"], count=row["count"]))
    return data
