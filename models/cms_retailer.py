from sqlalchemy import Column, Integer, TIMESTAMP
from databases.database import Base

class CMSCategoryRetailerLink(Base):
    __tablename__ = "summary_category_retailer_link"

    id = Column(Integer, primary_key=True, index=True)
    iCountryCode = Column(Integer, nullable=False)
    iCategoryCode = Column(Integer, nullable=False)
    iRetailerCode = Column(Integer, nullable=False)
    iRetailerHOCode = Column(Integer, nullable=False)
    deleted = Column(Integer, default=0)
    created = Column(TIMESTAMP, nullable=False)
    modified = Column(TIMESTAMP, nullable=False)
