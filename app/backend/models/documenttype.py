from pydantic import BaseModel


class DocumentType(BaseModel):
    shortName: str
    longName: str
    dbName: str
    domain: str
    defaultGraph: str
    typeHasLocation: bool = True
