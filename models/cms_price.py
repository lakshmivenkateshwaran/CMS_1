from sqlalchemy import Column, Integer, String, Text, Enum, Float, TIMESTAMP, SmallInteger
from databases.database import Base

class CMSCrawlingWebsiteProduct(Base):
    __tablename__ = "crawling_website_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    crawlWebsiteId = Column(Integer, nullable=False, default=0)
    batchId = Column(String(32), nullable=False)
    systemProductId = Column(Integer, nullable=False, default=0)
    systemAutoMatchedProductId = Column(Integer, nullable=False, default=0)
    systemPossibleMatchedProductId = Column(Integer, nullable=False)
    provisionalProductId = Column(Integer, nullable=False, default=0)
    restrictedUserProductId = Column(Integer, nullable=False, default=0)
    websiteInternalId = Column(String(255), nullable=False)
    modelCode = Column(String(255), nullable=False)
    skuCode = Column(String(255), nullable=False)
    uniqueIdentifierString = Column(Text, nullable=False)
    categoryId = Column(Integer, nullable=False, default=0)
    categoryName = Column(String(255), nullable=False)
    subCategoryId = Column(Integer, nullable=False, default=0)
    subCategoryName = Column(String(255), nullable=False)
    subCategoryChildId = Column(Integer, nullable=False, default=0)
    subCategoryChildName = Column(String(255), nullable=False, default='')
    manufacturerId = Column(Integer, nullable=False, default=0)
    manufacturerName = Column(String(255), nullable=False, default='')
    brandId = Column(Integer, nullable=False, default=0)
    brandName = Column(String(255), nullable=False, default='')
    productName = Column(String(255), nullable=False)
    price = Column(Float(asdecimal=True), nullable=False, default=0.0)
    isNPD = Column(SmallInteger, nullable=False, default=0)
    description = Column(Text, nullable=False)
    seller = Column(Text)
    status = Column(Enum('active', 'ignore'), nullable=False, default='active')
    isActive = Column(SmallInteger, nullable=False, default=0)
    isCategoryDeleted = Column(SmallInteger, nullable=False, default=0)
    matchedBy = Column(Integer, nullable=False, default=0)
    matchedDate = Column(TIMESTAMP, nullable=False)
    clearMatchBy = Column(Integer, nullable=False, default=0)
    clearMatchDate = Column(TIMESTAMP, nullable=False)
    ignoreBy = Column(Integer, nullable=False, default=0)
    ignoreDate = Column(TIMESTAMP, nullable=False)
    setActiveBy = Column(Integer, nullable=False, default=0)
    setActviveDate = Column(TIMESTAMP, nullable=False)
    deleted = Column(SmallInteger, nullable=False, default=0)
    created = Column(TIMESTAMP, nullable=False)
    modified = Column(TIMESTAMP, nullable=False)
