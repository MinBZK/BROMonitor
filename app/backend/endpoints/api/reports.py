from backend.queries.bronhouders import (
    get_quality_regimes_by_bronhouder,
    get_brondocumenten_count_by_bronhouder,
    get_bronhouders,
    get_top20,
    get_top20_since_date,
    get_bronhouders_over_time,
)
from backend.queries.documentTypes import (
    get_document_types,
    get_documents_over_time,
    get_document_delta,
    get_glds_updated,
    get_glds_start_update_count,
)
from backend.queries.metadata import get_youngest_object
from common.mongodb_utils import get_database
from backend.models.aggregate import DataModel
from backend.models.bronhouder import Bronhouder
from backend.models.dates import DatetimeModel
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from fastapi import APIRouter, Depends
from typing import List, Optional


router = APIRouter()


@router.get(
    "/brondocumenten-per-bronhouder", response_model=DataModel, include_in_schema=False
)
async def document_count_by_bronhouder(
    bronhoudertype: Optional[str] = None,
    gldstatus: Optional[str] = None,
    only_bronhouders: bool = True,
    db: AsyncIOMotorClient = Depends(get_database),
):
    return await get_brondocumenten_count_by_bronhouder(
        bronhoudertype, gldstatus, db, only_bronhouders=only_bronhouders
    )


@router.get(
    "/kwaliteitsregimes-per-bronhouder",
    response_model=DataModel,
    include_in_schema=False,
)
async def quality_regimes_by_bronhouder(
    bronhoudertype: str, db: AsyncIOMotorClient = Depends(get_database)
):
    return await get_quality_regimes_by_bronhouder(bronhoudertype, db)


@router.get("/documenten-over-tijd", response_model=DataModel, include_in_schema=False)
async def documents_over_time(
    object_type: str, db: AsyncIOMotorClient = Depends(get_database)
):
    return await get_documents_over_time(db, object_type)


@router.get(
    "/bronhouders-aanleveren-over-tijd",
    response_model=DataModel,
    include_in_schema=False,
)
async def bronhouders_over_time(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_bronhouders_over_time(db)


@router.get("/documenttypes", response_model=DataModel, include_in_schema=False)
async def document_types(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_document_types(db)


@router.get("/document-delta", response_model=DataModel, include_in_schema=False)
async def document_types(
    start_datum: Optional[datetime] = None,
    db: AsyncIOMotorClient = Depends(get_database),
):
    return await get_document_delta(db, start_datum)


@router.get("/bronhouders", response_model=List[Bronhouder], include_in_schema=False)
async def bronhouders(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_bronhouders(db)


@router.get("/top20", response_model=DataModel, include_in_schema=False)
async def top_20(
    type: Optional[str] = None, db: AsyncIOMotorClient = Depends(get_database)
):
    return await get_top20(db, type)


@router.get("/top20-sinds-datum", response_model=DataModel, include_in_schema=False)
async def top_20_since_date(
    start_datum: datetime, db: AsyncIOMotorClient = Depends(get_database)
):
    return await get_top20_since_date(db, start_datum)


@router.get(
    "/laatste-registratiedatum", response_model=DatetimeModel, include_in_schema=False
)
async def last_registrationdate(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_youngest_object(db)


@router.get("/nieuwe-glds", response_model=DataModel)
async def new_glds(
    db: AsyncIOMotorClient = Depends(get_database), date: Optional[datetime] = None
):
    return await get_glds_updated(db, date)


@router.get("/status-glds", response_model=DataModel)
async def glds_start_update_count(
    db: AsyncIOMotorClient = Depends(get_database), date: Optional[datetime] = None
):
    return await get_glds_start_update_count(db)
