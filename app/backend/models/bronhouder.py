from pydantic import BaseModel
from typing import Optional


class Bronhouder(BaseModel):
    name: str
    kvk: str
    identifier: Optional[str]
