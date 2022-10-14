from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from common.mongodb_utils import get_database
from queries.page_visits import log_page_visit, get_page_visits
from typing import List
from backend.models.aggregate import CountAggregate

router = APIRouter()


@router.get("/log-page-visit", include_in_schema=False)
async def track_url(url: str,
                    db: AsyncIOMotorClient = Depends(get_database)):
    await log_page_visit(db, url)


@router.get("/gebruiksstatistieken",
            response_model=List[CountAggregate],
            include_in_schema=False)
async def get_statistics(dagen: int = 7,
                         db: AsyncIOMotorClient = Depends(get_database)):
    return await get_page_visits(db, dagen)
