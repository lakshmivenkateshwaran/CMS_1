from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, SmallInteger
from sqlalchemy.sql import func
from databases.database import Base

class CMSClientReport(Base):
    __tablename__ = "cms_client_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userId = Column(Integer, nullable=False)
    clientId = Column(Integer, nullable=False, default=0)
    name = Column(String(255), nullable=False)
    worksheetPrefix = Column(String(255), default="")
    reportGraphTypeId = Column(Integer, default=1)
    reportTypeId = Column(Integer, default=1)
    reportTypeParameterId = Column(Integer, default=0)
    reportDataType = Column(Integer, default=2)
    status = Column(SmallInteger, default=0)
    preGenerate = Column(Enum('excel', 'powerpoint'), default='excel')
    PPRGenType = Column(Enum('weekly', 'monthly'), default='monthly')
    showScore = Column(SmallInteger, default=1)
    showSKU = Column(SmallInteger, default=1)
    showDesc = Column(SmallInteger, default=0)
    showNPD = Column(SmallInteger, default=0)
    PPshowAdCount = Column(SmallInteger, default=0)
    adCount = Column(SmallInteger, default=0)
    adCountType = Column(Enum('', 'total', 'unique'), default='')
    deleted = Column(SmallInteger, default=0)
    created = Column(TIMESTAMP, server_default=func.now())
    modified = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
