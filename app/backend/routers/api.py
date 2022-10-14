from fastapi import APIRouter

from backend.endpoints.api.reports import router as reports_router
from backend.endpoints.api.i18n import router as i18n_router
from backend.endpoints.api.bromonitor import router as bromonitor_router
from backend.endpoints.api.metadata import router as metadata_router
from backend.endpoints.api.page_visits import router as pagevisit_router

router = APIRouter()
router.include_router(reports_router, prefix="/rapporten", tags=["Rapporten"])
router.include_router(bromonitor_router, prefix="/bromonitor")
router.include_router(i18n_router, prefix="/i18n")
router.include_router(metadata_router, prefix="/metadata")
router.include_router(pagevisit_router, prefix='/pagevisits')
