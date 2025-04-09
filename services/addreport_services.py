from sqlalchemy.orm import Session
from models.category_model import Category as category
from models.sub_category_model import SubCategory as subcategory
from models.product_model import Product as product
from models.manufacturer_model import Manufacturer as manufacturer
from models.price_model import Price as price

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
