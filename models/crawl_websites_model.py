# models/crawling_websites.py
from sqlalchemy import Column, Integer, String, Enum, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from databases.database import Base

class CrawlingWebsite(Base):
    __tablename__ = "crawling_websites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    companyName = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    countryCode = Column(Integer, nullable=False)
    countryName = Column(String(255), nullable=False)
    pathToScript = Column(String(255), nullable=False)
    successfulCrawlDateTime = Column(TIMESTAMP, nullable=False)
    failedCrawlDateTime = Column(TIMESTAMP, nullable=False)
    status = Column(Enum("active", "scheduled", "inprogress", "suspend"), nullable=False, default="active")
    hideDashboard = Column(Boolean, nullable=False, default=False)
    deleted = Column(Boolean, nullable=False, default=False)
    created = Column(TIMESTAMP, nullable=False)
    modified = Column(TIMESTAMP, nullable=False)

   
    logs = relationship("CrawlingWebsiteLog", back_populates="website")
