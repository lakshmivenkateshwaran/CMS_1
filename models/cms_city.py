from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from databases.database import Base

class City(Base):
    __tablename__ = "tblCity"

    iCityCode = Column(Integer, primary_key=True, index=True)
    iCountryCode = Column(Integer)
    iStateCode = Column(Integer)
    sCityName = Column(String(255), nullable=False)
    bActivated = Column(Integer)
    bDeleted = Column(Integer)
    insertdate = Column(DateTime)
    changetime = Column(BigInteger)
    UpdatedDateTime = Column(DateTime)
