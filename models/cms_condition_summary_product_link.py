from sqlalchemy import Column, Integer, Float, TIMESTAMP
from databases.database import Base

class SummaryConditionOfSalesProductsLink(Base):
    __tablename__ = "summary_condition_of_sales_products_link"

    id = Column(Integer, primary_key=True, autoincrement=True)
    saleId = Column(Integer, nullable=False)
    iProductCode = Column(Integer, nullable=False)
    iBatchCode = Column(Integer, nullable=False)
    iBatchProductsCode = Column(Integer, nullable=False)
    dAdModifiedDate = Column(TIMESTAMP, nullable=False)
    mPrice = Column(Float(10, 2), nullable=False)
    iProductBrandCode = Column(Integer, nullable=False)
    iProductCatCode = Column(Integer, nullable=False)
    iProductSubCatCode = Column(Integer, nullable=False)
    deleted = Column(Integer, nullable=False, default=0)
    created = Column(TIMESTAMP, nullable=False)
    modified = Column(TIMESTAMP, nullable=False)
