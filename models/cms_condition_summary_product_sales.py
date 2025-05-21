from sqlalchemy import Column, Integer, String, TIMESTAMP
from databases.database import Base

class SummaryConditionOfSales(Base):
    __tablename__ = "summary_condition_of_sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    deleted = Column(Integer, nullable=False, default=0)
    created = Column(TIMESTAMP, nullable=False)
    modified = Column(TIMESTAMP, nullable=False)
