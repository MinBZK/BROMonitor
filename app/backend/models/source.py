from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class SourceTypeModel(BaseModel):
    type: str
    updated: Optional[datetime]


class SourceModel(BaseModel):
    name: str
    types: List[SourceTypeModel]
