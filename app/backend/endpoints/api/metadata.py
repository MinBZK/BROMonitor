from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List

from backend.queries.metadata import get_document_types
from backend.models.documenttype import DocumentType
from common.mongodb_utils import get_database

router = APIRouter()


@router.get("/documenttypes",
            response_model=List[DocumentType],
            include_in_schema=False)
async def document_types(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_document_types(db)
