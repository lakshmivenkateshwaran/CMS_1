from sqlalchemy import Column, Integer, String, TIMESTAMP
from databases.database import Base

class CMSSummaryDescriptionSplit(Base):
    __tablename__ = "summary_description_split"

    id = Column(Integer, primary_key=True, index=True)
    iCategoryCode = Column(Integer, nullable=False)
    iCountryCode = Column(Integer, nullable=False)
    CategoryDescriptionSplitID = Column(Integer, nullable=True)
    iSortOrder = Column(Integer, nullable=True)
    sDescriptionHeading = Column(String(50), nullable=True)
    deleted = Column(Integer, default=0)
    created = Column(TIMESTAMP, nullable=True)
    modified = Column(TIMESTAMP, nullable=True)
