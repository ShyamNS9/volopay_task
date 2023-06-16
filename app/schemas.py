from pydantic import BaseModel
from pydantic.validators import datetime


class TotalItem(BaseModel):
    start_date: datetime
    end_date: datetime
    department: str


class ResponseTotalItem(BaseModel):
    total_items: int

    class Config:
        orm_mode = True


class NthTotalItem(BaseModel):
    start_date: datetime
    end_date: datetime
    item_by: str
    n: int


class ResponseNthTotalItem(BaseModel):
    nth_most_total_item: str

    class Config:
        orm_mode = True


class PercentageSold(BaseModel):
    start_date: datetime
    end_date: datetime


class ResponsePercentageSold(BaseModel):
    percentage_of_department_wise_sold_items: dict

    class Config:
        orm_mode = True


class MonthlySale(BaseModel):
    product: str = "Apple"
    year: int


class ResponseMonthlySale(BaseModel):
    monthly_sales: list

    class Config:
        orm_mode = True