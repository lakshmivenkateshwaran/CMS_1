from sqlalchemy import Column, Integer, Float, ForeignKey
from databases.database import Base

class Price(Base):
    __tablename__ = "product_prices"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))
