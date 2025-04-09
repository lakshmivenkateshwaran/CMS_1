from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from databases.database import get_db
from services.addreport_services import get_filtered_data
from models.chart_model import ChartType
from models.category_model import Category
from models.sub_category_model import SubCategory
from models.product_model import Product
from models.manufacturer_model import Manufacturer


router = APIRouter()

@router.get("/report-data")
def get_report_data_all(
    report_name: str = Query(None),
    chart_type: str = Query(None),
    category: str = Query(None),
    subcategory: str = Query(None),
    product: str = Query(None),
    manufacturer: str = Query(None),
    db: Session = Depends(get_db)
):
    filters = {
        "report_name": report_name,
        "chart_type_id": chart_type,
        "category": category,
        "subcategory": subcategory,
        "product": product,
        "manufacturer": manufacturer
    }
    data = get_filtered_data(db, filters)
    return {"data": data}

#  Dropdown endpoints
@router.get("/chart-types")
def get_chart_types_dropdown(db: Session = Depends(get_db)):
    return db.query(ChartType).all()

@router.get("/categories")
def get_categories_dropdown(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/subcategories")
def get_subcategories_dropdown(category_id: int, db: Session = Depends(get_db)):
    return db.query(SubCategory).filter(SubCategory.category_id == category_id).all()

@router.get("/products")
def get_products_dropdown(subcategory_id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.subcategory_id == subcategory_id).all()

@router.get("/manufacturers")
def get_manufacturers_dropdown(product_id: int, db: Session = Depends(get_db)):
    return db.query(Manufacturer).filter(Manufacturer.product_id == product_id).all()
