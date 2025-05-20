from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from databases.database import Base

class MSTParameterMap(Base):
    __tablename__ = "mst_parameter_map"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String(255), nullable=False)
    map = Column(String(255), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    created = Column(TIMESTAMP, nullable=False, server_default="0000-00-00 00:00:00")
    modified = Column(TIMESTAMP, nullable=False, server_default="0000-00-00 00:00:00")
