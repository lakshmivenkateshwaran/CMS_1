from sqlalchemy import Column, Integer, String
from databases.database import Base 

class ClientReportSubType(Base):
    __tablename__ = "mst_client_report_type_sub_types"

    id = Column(Integer, primary_key=True, index=True)
    typeId = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)