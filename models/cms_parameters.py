from sqlalchemy import Column, Integer, String, Enum, SmallInteger, DateTime
from sqlalchemy.orm import relationship
from databases.database import Base
from datetime import datetime

# Model for MSTParameter (mst_parameter)
class CMSMSTParameter(Base):
    __tablename__ = "mst_parameter"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    type = Column(Enum('listMulti', 'money', 'decimal', 'text'), nullable=False)
    deleted = Column(SmallInteger, default=0)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)