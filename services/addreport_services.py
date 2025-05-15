from sqlalchemy.orm import Session
from models.category_model import Category as category
from models.sub_category_model import SubCategory as subcategory
from models.product_model import Product as product
from models.manufacturer_model import Manufacturer as manufacturer
from models.price_model import Price as price
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

def get_filtered_data(db: Session, filters: dict):
    query = db.query(price, manufacturer, product, subcategory, category)

    if filters.get("category"):
        query = query.join(subcategory, subcategory.category_id == category.id)\
                     .filter(category.name == filters["category"])

    if filters.get("subcategory"):
        query = query.join(product, product.subcategory_id == subcategory.id)\
                     .filter(subcategory.name == filters["subcategory"])

    if filters.get("product"):
        query = query.join(manufacturer, manufacturer.product_id == product.id)\
                     .filter(product.name == filters["product"])

    if filters.get("manufacturer"):
        query = query.join(price, price.manufacturer_id == manufacturer.id)\
                     .filter(manufacturer.name == filters["manufacturer"])

    results = query.all()

    # Convert query results to dicts that FastAPI can return as JSON
    return [
        {
            "price": row[0].price,
            "manufacturer": row[1].name,
            "product": row[2].name,
            "subcategory": row[3].name,
            "category": row[4].name
        } for row in results
    ]
# date type condition
def get_date_range_from_type(date_type: str):
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    if date_type.upper() == "MTD":
        start = today.replace(day=1)
        end = today

    elif date_type.upper() == "QTD":
        quarter = (current_month - 1) // 3 + 1
        start = datetime(current_year, 3 * (quarter - 1) + 1, 1)
        end = today

    elif date_type.upper() == "Q1":
        start = datetime(current_year, 1, 1)
        end = datetime(current_year, 3, 31)

    elif date_type.upper() == "Q2":
        start = datetime(current_year, 4, 1)
        end = datetime(current_year, 6, 30)

    elif date_type.upper() == "Q3":
        start = datetime(current_year, 7, 1)
        end = datetime(current_year, 9, 30)

    elif date_type.upper() == "Q4":
        start = datetime(current_year, 10, 1)
        end = datetime(current_year, 12, 31)

    elif date_type.lower() == "last_week":
        end = today
        start = today - timedelta(days=7)

    elif date_type.lower() == "last_month":
        end = today
        start = today - timedelta(days=30)
    
    elif date_type.lower() == "current_day":
        start = today
        end = today

    else:
        return None, None

    return start, end