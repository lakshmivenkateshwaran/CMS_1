from sqlalchemy import Column, Integer, String
from databases.database import Base

class MSTClientReportType(Base):
    __tablename__ = "mst_client_report_types"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
