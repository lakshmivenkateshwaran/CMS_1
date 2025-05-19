# models/crawling_website_logs.py

from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from databases.database import Base

class CrawlingWebsiteLog(Base):
    __tablename__ = "crawling_website_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    websiteId = Column(Integer, ForeignKey("crawling_websites.id"), nullable=False)
    batchId = Column(String(32), nullable=False)
    dateCrawl = Column(Integer, nullable=False)  # format: YYYYMMDD
    startDateTime = Column(TIMESTAMP, nullable=False)
    endDateTime = Column(TIMESTAMP, nullable=False)
    productsCrawled = Column(Integer, nullable=False, default=0)
    autoMatched = Column(Integer, nullable=False, default=0)
    matched = Column(Integer, nullable=False, default=0)
    possibleMatched = Column(Integer, nullable=False, default=0)
    notMatched = Column(Integer, nullable=False, default=0)
    ignored = Column(Integer, nullable=False, default=0)
    zeroPrice = Column(Integer, nullable=False, default=0)
    status = Column(Enum("success", "fail"), nullable=False, default="success")
    sendMailAlert = Column(Boolean, nullable=False, default=False)
    crawlType = Column(Enum("schedule", "manual"), nullable=False, default="schedule")
    deleted = Column(Boolean, nullable=False, default=False)
    created = Column(TIMESTAMP, nullable=False)
    modified = Column(TIMESTAMP, nullable=False)

    website = relationship("CrawlingWebsite", back_populates="logs")
