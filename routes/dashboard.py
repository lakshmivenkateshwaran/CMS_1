from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from security.security import get_current_user
from databases.database import get_db
from services.dashboard_service import fetch_sales_data
from schemas.sales_schema import SalesResponse
from typing import List

router = APIRouter()

@router.get("/sales-data", response_model=List[SalesResponse], dependencies=[Depends(get_current_user)])
def get_sales_data(db: Session = Depends(get_db)):
    return fetch_sales_data(db)
