from sqlalchemy import Column, Integer, String
from databases.database import Base  

class SalesData(Base):
    __tablename__ = "sales_data"
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String(20), nullable=False)
    sales = Column(Integer, nullable=False)
