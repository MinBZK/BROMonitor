# -*- coding: utf-8 -*-

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import secure
import logging
import os
import sys

from common.config import date_format, logging_format
from common.mongodb_utils import disconnect_mongo, connect_mongo
from backend.routers.api import router as api_router
from backend.endpoints.healthchecks import router as healthcheck_router

secure_headers = secure.Secure()

app = FastAPI(
    title="BRO Monitor",
    description="""Specificatie van bruikbare REST-endpoints binnen de BRO Monitor. 
                Responses van de API zijn geformatteerd als JSON objecten met 2 aanwezige velden.
                In het \"data\" veld bevindt zich een lijst van JSON objecten met de inhoudelijke data van de response.
                In het \"sources\" veld bevindt zich een lijst van bronnen die geraadpleegd zijn voor het genereren voor de response.
                Iedere bron bestaat uit een naam en een lijst van types die geraadpleegd zijn uit deze bron en de datum van de laatste wijziging binnen deze bron. """,
    docs_url="/api-docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_mongo)
app.add_event_handler("shutdown", disconnect_mongo)

app.include_router(api_router, prefix="/api")
app.include_router(healthcheck_router, prefix="/healthchecks")

logging.basicConfig(
    stream=sys.stdout,
    level=os.environ.get("LOGLEVEL", "INFO"),
    format=logging_format,
    datefmt=date_format,
)


@app.middleware("http")
async def set_secure_headers(request, call_next):
    """
    Middleware that adds security headers to each request.
    """
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response
