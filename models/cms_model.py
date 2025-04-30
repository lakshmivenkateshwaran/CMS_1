from sqlalchemy import Column, Integer, String, TIMESTAMP
from databases.database import Base

class CMSSummaryProductModel(Base):
    __tablename__ = "summary_product_model"

    id = Column(Integer, primary_key=True, index=True)
    iProductCode = Column(Integer, nullable=False)
    iProductCategoryCode = Column(Integer, nullable=False)
    iProductCatSubCode = Column(Integer, nullable=False)
    iProductCountryCode = Column(Integer, nullable=False)
    iProductBrandCode = Column(Integer, nullable=False)
    sProductModelNo = Column(String(255), nullable=False)
    sProductModelNo2 = Column(String(255), nullable=False)
    sProductModelNo3 = Column(String(255), nullable=False)
    sProductModelNo4 = Column(String(255), nullable=False)
    readableCreateDate = Column(Integer, nullable=False)
    bDiscontinued = Column(Integer, default=0)
    deleted = Column(Integer, default=0)
    created = Column(TIMESTAMP, nullable=False)
    modified = Column(TIMESTAMP, nullable=False)
