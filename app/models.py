from pydantic import BaseModel
from typing import List
from datetime import datetime


class ValidateIPResponse(BaseModel):
    status: bool


class LookupResponse(BaseModel):
    ipv4_addresses: List[str]


class QueryResponse(BaseModel):
    id: int
    domain: str
    ipv4_addresses: str
    created_at: datetime


class HistoryResponse(BaseModel):
    __root__: List[QueryResponse]
