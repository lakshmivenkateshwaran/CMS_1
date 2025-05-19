from sqlalchemy import Column, Integer, String
from databases.database import Base  

class ChartType(Base):
    __tablename__ = "mst_client_report_graph_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)