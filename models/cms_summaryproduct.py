from sqlalchemy import Column, Integer, String, Text, Numeric, TIMESTAMP
from databases.database import Base

class CMSSummaryProduct(Base):
    __tablename__ = "summary_products"

    id = Column(Integer, primary_key=True, index=True)
    iProductCode = Column(Integer, nullable=False)
    iProductCategoryCode = Column(Integer, nullable=False)
    iProductCatSubCode = Column(Integer, nullable=False)
    iProductCountryCode = Column(Integer, nullable=False)
    iProductBrandCode = Column(Integer, nullable=False)
    sProductModelNo = Column(String(255), nullable=False)
    sProductModelNo2 = Column(String(255), nullable=False)
    sProductDesc = Column(Text, nullable=False)
    sProductOneLineDesc = Column(Text, nullable=False)
    sProductPicture = Column(String(500), nullable=False)
    mRRP = Column(Numeric(10, 2), nullable=False)
    mMin = Column(Numeric(10, 2), nullable=False)
    mAve = Column(Numeric(10, 2), nullable=False)
    mMax = Column(Numeric(10, 2), nullable=False)
    readableCreateDate = Column(Integer, nullable=False)
    bDiscontinued = Column(Integer, default=0)
    deleted = Column(Integer, default=0)
    created = Column(TIMESTAMP, nullable=False)
    modified = Column(TIMESTAMP, nullable=False)
