# models/retailer.py
from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger
from databases.database import Base

class CMSRetailer(Base):
    __tablename__ = "tblRetailer"

    iRetailerHOCode = Column(Integer, primary_key=True)
    iRetailerCode = Column(Integer)
    sRetailerName = Column(String(50))
    iRetailerCountryCode = Column(Integer)
    iRetailerStateCode = Column(Integer)
    iRetailerCityCode = Column(Integer)
    sRetailerContactName = Column(String(50))
    sRetailerContactPhoneNo = Column(String(50))
    sRetailerNote = Column(Text)
    bDeleted = Column(Integer)
    insertdate = Column(DateTime)
    changetime = Column(BigInteger)
    UpdatedDateTime = Column(DateTime)
