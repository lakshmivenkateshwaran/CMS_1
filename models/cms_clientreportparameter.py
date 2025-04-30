from sqlalchemy import Column, Integer, String, Enum, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from databases.database import Base
from datetime import datetime


class CMSClientReportParameter(Base):
    __tablename__ = "cms_client_reports_parameters"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    reportId = Column(Integer, nullable=False)
    parameterId = Column(Integer, ForeignKey('mst_parameter.id'), nullable=False)
    value = Column(String(1000), nullable=False)
    deleted = Column(SmallInteger, default=0)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships to the other tables
    parameter = relationship("CMSMSTParameter", backref="report_parameters")