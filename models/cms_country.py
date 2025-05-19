from sqlalchemy import Column, Integer, String
from databases.database import Base

class CMSCountry(Base):
    __tablename__ = "tbl_country"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), nullable=False)
    country_code = Column(Integer, nullable=False, unique=True)
