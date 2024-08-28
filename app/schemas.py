from pydantic import BaseModel


class HealthStatus(BaseModel):
    status: str


class Status(BaseModel):
    date: int
    kubernetes: bool
    version: str


class ValidateIPRequest(BaseModel):
    ip: str
