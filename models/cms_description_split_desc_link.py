from sqlalchemy import Column, Integer, String, TIMESTAMP
from databases.database import Base

class CMSSummaryDescriptionSplitDescriptionLink(Base):
    __tablename__ = "summary_description_split_description_link"

    id = Column(Integer, primary_key=True, index=True)
    summaryDescriptionSplitId = Column(Integer, nullable=False)
    descriptionField = Column(String(250), nullable=False)
    deleted = Column(Integer, default=0)
    created = Column(TIMESTAMP, nullable=True)
    modified = Column(TIMESTAMP, nullable=True)
