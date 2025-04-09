from sqlalchemy.orm import Session
from models.sales_model import SalesData

def fetch_sales_data(db: Session):
    return db.query(SalesData).all()
