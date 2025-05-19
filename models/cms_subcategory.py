from sqlalchemy import Column, Integer, String, DateTime, BigInteger, TIMESTAMP, ForeignKey
from databases.database import Base

class CMSSubCategory(Base):
    __tablename__ = "tblCatSub"

    iCatSubCode = Column(Integer, primary_key=True, index=True)
    iCategoryCode = Column(Integer, ForeignKey("tblCategory.iCategoryCode"), nullable=False)
    sCatSubName = Column(String(255), nullable=False)
    bDeleted = Column(Integer, nullable=False)
    insertdate = Column(DateTime)
    changetime = Column(BigInteger, nullable=False)
    UpdatedDateTime = Column(TIMESTAMP, nullable=False)
