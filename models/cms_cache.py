from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from databases.database import Base 

class CMSCache(Base):
    __tablename__ = "cache"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reportId = Column(Integer, nullable=False, default=0)
    keyDetails = Column(String(255), nullable=False)
    keyContents = Column(Text, nullable=False)
    data = Column(Text, nullable=False)
    adCountData = Column(Text, nullable=False)
    fileGenerated = Column(String(500), nullable=False)
    lastCalculateDate = Column(Integer, nullable=False)
    deleted = Column(Integer, nullable=False, default=0)
    created = Column(TIMESTAMP, nullable=False, default=func.now())
    modified = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())
