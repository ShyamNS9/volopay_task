from datetime import date
from typing import List
from fastapi import Depends, APIRouter, Query
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from app.database import get_db_connection as get_db
from app import models, schemas

api_router = APIRouter(
    prefix="/api",
    tags=['api']
)


@api_router.get("/total_items", response_model=schemas.ResponseTotalItem)
async def get_item(
        start_date: date = Query(default="2022-07-15", description="Enter starting date here as YYYY-MM-DD"),
        end_date: date = Query(default="2022-09-15", description="Enter ending date here as YYYY-MM-DD"),
        department: str = Query(default="HR", description="Enter department like 'HR'"),
        db: Session = Depends(get_db)):
    total_items = db.query(models.SoftwareDetails).filter(
        models.SoftwareDetails.date >= start_date,
        models.SoftwareDetails.date <= end_date,
        models.SoftwareDetails.department == department
    ).count()

    return {"total_items": total_items}


@api_router.get("/nth_most_total_item", response_model=schemas.ResponseNthTotalItem)
async def get_nth_most_total_item(
        start_date: date = Query(default="2022-07-15", description="Enter starting date here as YYYY-MM-DD"),
        end_date: date = Query(default="2022-09-15", description="Enter ending date here as YYYY-MM-DD"),
        item_by: str = Query(default="quantity",
                             description="Enter How you want to sort the data like 'quantity' **OR** 'price'"),
        n: int = Query(default=1, description="In descending order what ranked item you want to fetch"),
        db: Session = Depends(get_db)):
    if item_by == "quantity":
        column_to_order = func.sum(models.SoftwareDetails.seats)
    elif item_by == "price":
        column_to_order = func.sum(models.SoftwareDetails.amount)
    else:
        return {"error": "Invalid item_by parameter. Valid values are 'quantity' or 'price'."}

    result = db.query(models.SoftwareDetails.software, column_to_order.label("total")).filter(
        models.SoftwareDetails.date >= start_date,
        models.SoftwareDetails.date <= end_date
    ).group_by(models.SoftwareDetails.software).order_by(column_to_order.desc()).limit(n).all()

    if len(result) < n:
        return {"error": f"Requested n ({n}) is greater than the number of available items."}

    nth_most_total_item = result[-1].software

    return {"nth_most_total_item": nth_most_total_item}


@api_router.get("/percentage_of_department_wise_sold_items", response_model=schemas.ResponsePercentageSold)
async def get_percentage_of_department_wise_sold_items(
        start_date: date = Query(default="2022-07-15", description="Enter starting date here as YYYY-MM-DD"),
        end_date: date = Query(default="2022-09-15", description="Enter ending date here as YYYY-MM-DD"),
        db: Session = Depends(get_db)):
    result = db.query(
        models.SoftwareDetails.department,
        func.sum(models.SoftwareDetails.seats).label("total_seats")
    ).filter(
        models.SoftwareDetails.date >= start_date,
        models.SoftwareDetails.date <= end_date
    ).group_by(models.SoftwareDetails.department).all()

    total_seats_sold = sum(row.total_seats for row in result)
    percentage_of_department_wise_sold_items = {
        row.department: (row.total_seats / total_seats_sold) * 100
        for row in result
    }

    return {"percentage_of_department_wise_sold_items": percentage_of_department_wise_sold_items}


@api_router.get("/monthly_sales", response_model=schemas.ResponseMonthlySale)
async def get_monthly_sales(
        product: str = Query(default="Apple",
                             description="Enter the product name you want to fetch like 'Apple'"),
        year: int = Query(default=2022, description="Enter for what year you want to fetch like 'YYYY'"),
        db: Session = Depends(get_db)):
    result = db.query(
        extract('month', models.SoftwareDetails.date).label("month"),
        func.sum(models.SoftwareDetails.amount).label("total_sales")
    ).filter(
        models.SoftwareDetails.software == product,
        extract('year', models.SoftwareDetails.date) == year
    ).group_by(extract('month', models.SoftwareDetails.date)).all()
    monthly_sales = [0] * 12
    for item in result:
        monthly_sales[int(item[0]) - 1] = item[1]

    return {"monthly_sales": monthly_sales}
