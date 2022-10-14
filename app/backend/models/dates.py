from pydantic import BaseModel
from datetime import datetime


class DatetimeModel(BaseModel):
    date: datetime


class DatesModel(BaseModel):
    dates: list  # list of dates
