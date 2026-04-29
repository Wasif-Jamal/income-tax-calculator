from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.tax import TaxRequest, TaxResponse, TaxRecordResponse
from app.services.tax_service import calculate_tax
from app.models.tax import TaxRecord
from app.db.database import get_db
from app.repository.tax_repository import create_tax_record, get_all_records

router = APIRouter()

@router.post("/calculate-tax", response_model=TaxResponse)
def calculate_tax_api(payload: TaxRequest, db: Session = Depends(get_db)):
    tax = calculate_tax(payload.income, payload.hra, payload.regime)

    create_tax_record(
        db,
        payload.income,
        payload.hra,
        payload.regime,
        tax
    )

    return {'tax': tax}

@router.get("/history", response_model=List[TaxRecordResponse])
def get_tax_history(db: Session = Depends(get_db)):
    records = get_all_records(db)
    return records