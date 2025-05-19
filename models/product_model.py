from sqlalchemy import Column, Integer, String, ForeignKey
from databases.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
