from fastapi import APIRouter
import os
import json

router = APIRouter()


@router.get("/nl-NL", include_in_schema=False)
async def get_dutch_language():
    file_path = os.path.dirname(__file__) + '/../../i18n/nl-NL.json'
    with open(file_path, encoding="utf-8") as json_file:
        return json.load(json_file)
