from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint
from pydantic.validators import datetime


class TotalItem(BaseModel):
    start_date: datetime
    end_date: datetime
    department: str


class NthTotalItem(BaseModel):
    start_date: datetime
    end_date: datetime
    item_by: str
    n: int


class PercentageSold(BaseModel):
    start_date: datetime
    end_date: datetime


class MonthlySale(BaseModel):
    product: str
    year: int
