from sqlalchemy import Column, Integer, TIMESTAMP
from databases.database import Base

class CMSSummaryDescriptionSplitProductLink(Base):
    __tablename__ = "summary_description_split_product_link"

    id = Column(Integer, primary_key=True, index=True)
    summaryDescriptionSplitId = Column(Integer, nullable=False)
    summaryDescriptionSplitDescriptionId = Column(Integer, nullable=False)
    iProductCode = Column(Integer, nullable=False)
    deleted = Column(Integer, default=0)
    created = Column(TIMESTAMP, nullable=True)
    modified = Column(TIMESTAMP, nullable=True)
