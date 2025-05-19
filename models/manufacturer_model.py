from sqlalchemy import Column, Integer, String, ForeignKey
from databases.database import Base

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
