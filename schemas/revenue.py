from pydantic import BaseModel
from datetime import date


class RevenueCreate(BaseModel):
    month: date
    revenue: float


class RevenueResponse(BaseModel):
    id: int
    month: date
    revenue: float

    class Config:
        from_attributes = True