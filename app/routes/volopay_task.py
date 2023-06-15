from fastapi import Depends, APIRouter
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from app.database import get_db_connection as get_db
from app import models, schemas

api_router = APIRouter(
    prefix="/api",
    tags=['api']
)


@api_router.get("/total_items")
async def get_item(request: schemas.TotalItem, db: Session = Depends(get_db)):
    total_items = db.query(models.SoftwareDetails).filter(
        models.SoftwareDetails.date >= request.start_date,
        models.SoftwareDetails.date <= request.end_date,
        models.SoftwareDetails.department == request.department
    ).count()
    print(total_items)
    return {"total_items": total_items}


@api_router.get("/nth_most_total_item")
def get_nth_most_total_item(request: schemas.NthTotalItem, db: Session = Depends(get_db)):
    if request.item_by == "quantity":
        column_to_order = func.sum(models.SoftwareDetails.seats)
    elif request.item_by == "price":
        column_to_order = func.sum(models.SoftwareDetails.amount)
    else:
        return {"error": "Invalid item_by parameter. Valid values are 'quantity' or 'price'."}

    result = db.query(models.SoftwareDetails.software, column_to_order.label("total")).filter(
        models.SoftwareDetails.date >= request.start_date,
        models.SoftwareDetails.date <= request.end_date
    ).group_by(models.SoftwareDetails.software).order_by(column_to_order.desc()).limit(request.n).all()

    if len(result) < request.n:
        return {"error": f"Requested n ({request.n}) is greater than the number of available items."}

    nth_most_total_item = result[-1].software

    return {"nth_most_total_item": nth_most_total_item}


@api_router.get("/percentage_of_department_wise_sold_items")
def get_percentage_of_department_wise_sold_items(request: schemas.PercentageSold, db: Session = Depends(get_db)):
    result = db.query(
        models.SoftwareDetails.department,
        func.sum(models.SoftwareDetails.seats).label("total_seats")
    ).filter(
        models.SoftwareDetails.date >= request.start_date,
        models.SoftwareDetails.date <= request.end_date
    ).group_by(models.SoftwareDetails.department).all()

    total_seats_sold = sum(row.total_seats for row in result)
    percentage_of_department_wise_sold_items = {
        row.department: (row.total_seats / total_seats_sold) * 100
        for row in result
    }

    return {"percentage_of_department_wise_sold_items": percentage_of_department_wise_sold_items}


@api_router.get("/monthly_sales")
def get_monthly_sales(request: schemas.MonthlySale, db: Session = Depends(get_db)):
    result = db.query(
        extract('month', models.SoftwareDetails.date).label("month"),
        func.sum(models.SoftwareDetails.amount).label("total_sales")
    ).filter(
        models.SoftwareDetails.software == request.product,
        extract('year', models.SoftwareDetails.date) == request.year
    ).group_by(extract('month', models.SoftwareDetails.date)).all()

    print(result)

    monthly_sales = [0] * 12
    for item in result:
        monthly_sales[int(item[0]) - 1] = item[1]

    return monthly_sales
