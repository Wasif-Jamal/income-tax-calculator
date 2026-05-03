from sqlalchemy import Column, Integer, Float, String
from app.config.db_config import Base

class TaxRecord(Base):
    __tablename__ = 'tax_records'

    id = Column(Integer, primary_key=True, index=True)
    income = Column(Float, nullable=False)
    hra = Column(Float, nullable=False)
    regime = Column(String, nullable=False)
    tax = Column(Float, nullable=False)
