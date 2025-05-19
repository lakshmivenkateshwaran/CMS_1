from pydantic import BaseModel

class SalesResponse(BaseModel):
    month: str
    sales: int

    class Config:
        orm_mode = True
