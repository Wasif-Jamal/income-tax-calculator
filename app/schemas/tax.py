from pydantic import BaseModel, ConfigDict

class TaxRequest(BaseModel):
    income: float
    hra: float
    regime: str # 'old' or 'new'

class TaxResponse(BaseModel):
    tax: float

class TaxRecordResponse(BaseModel):
    id: int
    income: float
    hra: float
    regime: str
    tax: float

    model_config = ConfigDict(from_attributes=True)