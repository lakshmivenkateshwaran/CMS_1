from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, Boolean, DateTime, Text
from databases.database import Base

class CMSCrawlingWebsiteProductsCrawlHistory(Base):
    __tablename__ = 'crawling_website_products_crawl_history'

    id = Column(Integer, primary_key=True)
    crawlWebsiteId = Column(Integer)
    crawlDate = Column(Integer)
    searializeProductCodes = Column(Text)
    deleted = Column(Boolean)
    created = Column(DateTime)
    modified = Column(DateTime)