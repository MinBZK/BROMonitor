from typing import List
from fastapi import APIRouter, Depends, Response
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from pymongo import MongoClient
from backend.utils.documentTypes import document_type_registry
from common.mongodb_utils import get_database
from backend.utils.pingdom import generate_pingdom_xml

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", include_in_schema=False)
async def healthcheck_status(db: AsyncIOMotorClient = Depends(get_database)):

    log.info(f"In healthcheck_status ")
    errors = ""
    try:
        for doc_type in document_type_registry.get_short_names():
            short_name = doc_type.lower()
            source = await db.bro.source.find_one({"type": short_name})
            if not source:
                log.warning(
                    f"Unable to retrieve source document for type: {short_name}")
                errors += f"Unable to retrieve source document for type: {short_name}. "
            elif source['status'] != "OK":
                errors += f"ETL {source['status']} for {short_name}. "
    except BaseException as ex:
        errors += f"MongoDb error. {ex} "

    if len(errors) > 0:
        data = generate_pingdom_xml(errors, 503)
        log.error(errors)
    else:
        data = generate_pingdom_xml("OK", 200)

    return Response(content=data, media_type="application/xml")
