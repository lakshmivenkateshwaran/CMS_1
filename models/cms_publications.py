from sqlalchemy import Column, Integer, String, Float, Text, DateTime, BigInteger, TIMESTAMP
from databases.database import Base

class CMSNewspaper(Base):
    __tablename__ = "tblNewspaper"

    iNewspaperCode = Column(Integer, primary_key=True, index=True)
    sNewspaperPublication = Column(String(50))
    sNewspaperName = Column(String(255), nullable=False)
    iNewspaperCountryCode = Column(Integer, nullable=False)
    iNewspaperStateCode = Column(Integer, nullable=False)
    iNewspaperCityCode = Column(Integer, nullable=False)
    fNewspaperPubFactor = Column(Float, nullable=False)
    sNewspaperNote = Column(Text)
    bDeleted = Column(Integer, nullable=False)
    insertdate = Column(DateTime)
    changetime = Column(BigInteger, nullable=False)
    UpdatedDateTime = Column(TIMESTAMP, nullable=False)
