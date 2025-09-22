from typing import List
from fastapi import APIRouter, Depends, Response
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import logging
from pymongo import MongoClient
from backend.utils.documentTypes import document_type_registry
from common.mongodb_utils import get_database
from backend.utils.pingdom import generate_pingdom_xml
from backend.mailing.mailing import send_notificatie_mail

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", include_in_schema=False)
async def healthcheck_status(db: AsyncIOMotorClient = Depends(get_database)):

    log.info(f"In healthcheck_status ")
    errors = ""
    errors_to_notify = []
    try:
        for doc_type in document_type_registry.get_short_names():
            short_name = doc_type.lower()
            source = await db.bro.source.find_one({"type": short_name})
            if not source:
                log.warning(
                    f"Unable to retrieve source document for type: {short_name}")
                errors += f"Unable to retrieve source document for type: {short_name}. "
            elif source['status'] != "OK" and (
                (source.get("notified_at", None) is None)
                ):
                errors_to_notify.append(f"ETL {source['status']} for {short_name}.")
            elif source['status'] == "OK" and source.get("notified_at", None) is not None:
                db.bro.source.update_one(
                    {"type": short_name},
                    {"$unset": {"notified_at": ""}},
                    upsert=True)

        if errors_to_notify:
            receivers = ["devops@ictu.nl"]
            subject = "ETL status"

            message = "Beste beheerder,\n\nNieuwe foutmelding(en) in de ETL:\n"
            for error in errors_to_notify:
                message += f"- {error}\n"
            message += "\nDit is een automatisch gegenereerd bericht."

            send_notificatie_mail(receivers, subject, message)
            
            cursor = db.bro.source.find({"status": {"$ne": "OK"}})
            async for doc in cursor:
                await db.bro.source.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"notified_at": datetime.now()}},
                    upsert=True,
                )

    except BaseException as ex:
        errors += f"Error: {ex}"

    if len(errors) > 0:
        data = generate_pingdom_xml(errors, 503)
        log.error(errors)
    else:
        data = generate_pingdom_xml("OK", 200)

    return Response(content=data, media_type="application/xml")
