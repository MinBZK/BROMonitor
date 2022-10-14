from dataclasses import dataclass
from datetime import datetime


@dataclass
class Feed(object):
    filename: str
    zip_url: str
    zip_size_in_bytes: int
    updated: datetime
