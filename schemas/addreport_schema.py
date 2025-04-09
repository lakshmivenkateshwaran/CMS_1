from pydantic import BaseModel
from typing import Optional

class ReportFilter(BaseModel):
    report_name: Optional[str]
    chart_type_id: Optional[int]
    category: Optional[str]
    subcategory: Optional[str]
    product: Optional[str]
    manufacturer: Optional[str]
