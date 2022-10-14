from backend.models.aggregate import BromonitorModel, BromonitorModelRecent, SourceModel
from backend.models.dates import DatesModel
from backend.queries.bromonitor import (
    get_bromonitor_recent,
    get_bromonitor_embedded,
    get_bromonitor_dates,
    get_bromonitor_by_date,
    get_bromonitor_timestamp,
)
from common.mongodb_utils import get_database
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter, Depends
from datetime import datetime


router = APIRouter()


@router.get("/bromonitor", response_model=BromonitorModel, include_in_schema=False)
async def bromonitor_recent(
    datum: datetime, db: AsyncIOMotorClient = Depends(get_database)
):
    return await get_bromonitor_by_date(db, datum)


@router.get(
    "/bromonitor-embedded", response_model=BromonitorModel, include_in_schema=False
)
async def bromonitor_recent(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_bromonitor_embedded(db)


@router.get(
    "/bromonitor-recent", response_model=BromonitorModelRecent, include_in_schema=False
)
async def bromonitor_recent(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_bromonitor_recent(db)


@router.get("/bromonitor-datums", response_model=DatesModel, include_in_schema=False)
async def bromonitor_dates(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_bromonitor_dates(db)


@router.get(
    "/bromonitor-timestamp", response_model=SourceModel, include_in_schema=False
)
async def bromonitor_recent(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_bromonitor_timestamp(db)
