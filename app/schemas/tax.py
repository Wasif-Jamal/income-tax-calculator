from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

class TaxRequest(BaseModel):
    income: float = Field(..., ge=0)
    hra: float = Field(..., ge=0)
    regime: Literal['old', 'new']

class TaxResponse(BaseModel):
    tax: float

class TaxRecordResponse(BaseModel):
    id: int
    income: float
    hra: float
    regime: str
    tax: float

    model_config = ConfigDict(from_attributes=True)