from motor.motor_asyncio import AsyncIOMotorClient

from common.config import (
    MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT)


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_mongo():
    db.client = AsyncIOMotorClient(str(MONGODB_URL),
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)


async def disconnect_mongo():
    db.client.close()
