from sqlalchemy.orm import Session
from app.models.tax import TaxRecord

def create_tax_record(db: Session, income: float, hra: float, regime: str, tax: float):
    record = TaxRecord (
        income = income,
        hra = hra,
        regime = regime,
        tax = tax
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_records(db: Session):
    return db.query(TaxRecord).all()