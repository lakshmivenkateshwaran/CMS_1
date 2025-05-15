# schemas/website_log.py
from pydantic import BaseModel

class WebsiteCrawlSummary(BaseModel):
    websiteName: str
    totalProductsCrawled: int
