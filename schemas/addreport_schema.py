from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class ReportFilter(BaseModel):
    report_name: Optional[str]
    chart_type_id: Optional[int]
    category: Optional[str]
    subcategory: Optional[str]
    product: Optional[str]
    manufacturer: Optional[str]

class SaveReportView(BaseModel):
    client_id: Optional[int] = 0 
    report_name: str  
    country: str
    category: str
    subcategory: str
    brand: str
    model: str
    retailer: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    date_type: Optional[str] = None

class ReportSummary(BaseModel):
    id: int
    name: str
    created: datetime

    class Config:
        orm_mode = True


    






