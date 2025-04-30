from pydantic import BaseModel, EmailStr

class ShareReportRequest(BaseModel):
    email: EmailStr
