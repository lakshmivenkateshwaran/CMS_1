from sqlalchemy import Column, Integer, SmallInteger, DateTime
from sqlalchemy.orm import relationship
from databases.database import Base  

class CMSAccountsCategoryLinks(Base):
    __tablename__ = 'accounts_category_links'

    id = Column(Integer, primary_key=True, index=True)
    accountId = Column(Integer, index=True)
    countryId = Column(Integer, index=True)
    categoryId = Column(Integer, index=True)
    clientId = Column(Integer)
    bannerAdFlag = Column(SmallInteger)
    deleted = Column(SmallInteger, default=0)
    created = Column(DateTime)
    modified = Column(DateTime)
