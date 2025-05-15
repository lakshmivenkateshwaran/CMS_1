from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, TIMESTAMP
from databases.database import Base

class CMSManufacturerBrand(Base):
    __tablename__ = "tblManufacturerBrand"

    iManBrandCode = Column(Integer, primary_key=True, index=True)
    iManCode = Column(Integer, nullable=False)
    sBrandName = Column(String(100), nullable=False)
    sBranchNote = Column(Text)
    bDeleted = Column(Integer, nullable=False)
    insertdate = Column(DateTime)
    changetime = Column(BigInteger, nullable=False)
    UpdatedDateTime = Column(TIMESTAMP, nullable=False)
