from sqlalchemy import Column, Integer, String, DateTime, BigInteger, TIMESTAMP
from databases.database import Base

class CMSCategory(Base):
    __tablename__ = "tblCategory"

    iCategoryCode = Column(Integer, primary_key=True, index=True)
    sCategoryName = Column(String(255), nullable=False)
    sAttrib1Context = Column(String(100))
    sAttrib2Context = Column(String(100))
    sAttrib3Context = Column(String(100))
    sAttrib4Context = Column(String(100))
    sAttrib5Context = Column(String(100))
    iVariancePercentage = Column(Integer, nullable=False)
    bDeleted = Column(Integer, nullable=False)
    iRoundingPlaces = Column(Integer)
    insertdate = Column(DateTime)
    changetime = Column(BigInteger, nullable=False)
    UpdatedDateTime = Column(TIMESTAMP, nullable=False)
