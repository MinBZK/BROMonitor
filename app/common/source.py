from dataclasses import dataclass
from datetime import datetime


@dataclass
class Source(object):
    id: str
    name: str
    type: str
    url: str
    updated: datetime
    last_queried: datetime
    etl_status: str
    last_loaded: datetime
