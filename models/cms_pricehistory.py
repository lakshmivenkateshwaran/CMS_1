from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, Boolean
from databases.database import Base

class CMSProductPriceHistory(Base):
    __tablename__ = "crawling_website_products_price_history"

    id = Column(Integer, primary_key=True, index=True)
    productId = Column(Integer, nullable=False)
    crawlWebsiteId = Column(Integer, nullable=False)
    batchId = Column(String(32), nullable=False)
    price = Column(Float, nullable=False)
    referenceDate = Column(Integer, nullable=False) 
    deleted = Column(Boolean, default=False)
    created = Column(TIMESTAMP)
    modified = Column(TIMESTAMP)
