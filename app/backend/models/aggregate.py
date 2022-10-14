from typing import List, Optional, Tuple
from pydantic import BaseModel

from backend.models.source import SourceModel


class DataModel(BaseModel):
    data: list  # list of aggregates
    sources: List[SourceModel]


class BromonitorModel(BaseModel):
    date: str
    html: str


class BromonitorModelRecent(BromonitorModel):
    static: dict
    static_data: dict


class CountAggregate(BaseModel):
    key: str
    count: int


class QualityRegimeAggregate(BaseModel):
    bronhouder: str
    identifier: Optional[str]
    quality_regimes: List[CountAggregate]


class BronhouderAndType(BaseModel):
    kvk: str
    naam: Optional[str]
    identifier: Optional[str]
    type: Optional[str]
    status: Optional[str]


class PerBronhouderCountAggregate(BaseModel):
    key: BronhouderAndType
    count: int


class ObjectTypeRegimeAggregate(BaseModel):
    object_type: str
    quality_regime: str
    count: int


class Top20Aggregate(BaseModel):
    bronhouder: str
    object_type: str
    imbro_count: int
    imbroa_count: int


class BronhoudersPerMonth(BaseModel):
    kvk: str
    naam: str
    identifier: str
    monthyear: Tuple[int, int]
    object_type: str
    count: int
