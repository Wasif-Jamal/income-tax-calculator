import pytest
from fastapi.testclient import TestClient
from app.exceptions.custom_exceptions import InvalidRegimeError
from app.services.tax_service import TaxCalculator
from app.config.db_config import Base, get_engine


# ------------------------
# BASIC FUNCTIONAL TESTS
# ------------------------

def test_old_regime_basic():
    calc = TaxCalculator(1000000, 0, "old")
    tax = calc.calculate()

    # manual calc:
    # taxable income = 10L - 50k = 9.5L
    # 2.5L–5L → 5% = 12,500
    # 5L–10L → 20% = 90,000
    assert tax == 102500


def test_new_regime_basic():
    calc = TaxCalculator(1400000, 0, "new")
    tax = calc.calculate()

    # slab-wise:
    # 4L–8L → 5% = 20,000
    # 8L–12L → 10% = 40,000
    # 12L–16L → 15% = 18750
    assert tax == 78750


# ------------------------
# HRA + STANDARD DEDUCTION
# ------------------------

def test_taxable_income_with_hra_old():
    calc = TaxCalculator(500000, 100000, "old")
    # taxable = 500000 - 100000 - 50000 = 350000
    assert calc._get_taxable_income() == 350000


def test_taxable_income_with_hra_new():
    calc = TaxCalculator(500000, 100000, "new")
    # taxable = 500000 - 100000 - 75000 = 325000
    assert calc._get_taxable_income() == 325000


# ------------------------
# REBATE TESTS
# ------------------------

def test_old_regime_rebate():
    calc = TaxCalculator(500000, 0, "old")
    assert calc.calculate() == 0


def test_new_regime_rebate():
    calc = TaxCalculator(1200000, 0, "new")
    assert calc.calculate() == 0


# ------------------------
# EDGE CASES
# ------------------------

def test_zero_income():
    calc = TaxCalculator(0, 0, "old")
    assert calc.calculate() == 0


def test_negative_taxable_income():
    calc = TaxCalculator(50000, 100000, "old")
    assert calc.calculate() == 0


# ------------------------
# HIGH INCOME CASES
# ------------------------

def test_high_income_old():
    calc = TaxCalculator(2000000, 0, "old")
    tax = calc.calculate()

    assert tax > 0
    assert isinstance(tax, float)


def test_high_income_new():
    calc = TaxCalculator(2000000, 0, "new")
    tax = calc.calculate()

    assert tax > 0
    assert isinstance(tax, float)


# ------------------------
# INVALID INPUT
# ------------------------

def test_invalid_regime():
    with pytest.raises(ValueError):
        calc = TaxCalculator(500000, 0, "invalid")
        calc.calculate()


# ------------------------
# ROUNDING
# ------------------------

def test_tax_rounding():
    calc = TaxCalculator(1423673, 0, "new")
    tax = calc.calculate()

    assert isinstance(tax, float)
    assert round(tax, 2) == tax

# ------------------------
# INVALID REGIME
# ------------------------

def test_invalid_regime():
    calc = TaxCalculator(500000, 0, "invalid")

    with pytest.raises(InvalidRegimeError) as exc:
        calc.calculate()
    print(f'INVALIDREGIMEERROR: {str(exc.value)}')

    assert "Invalid regime" in str(exc.value)


# ------------------------
# UNEXPECTED ERROR
# ------------------------

def test_unexpected_error():
    # Passing wrong type to trigger unexpected exception
    calc = TaxCalculator("abc", 0, "old")

    with pytest.raises(TypeError) as exc:
        calc.calculate()

    assert isinstance(exc.value, TypeError)

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("DB_URL", "sqlite:///:memory:")
    get_engine.cache_clear()

    from app.main import app

    engine = get_engine()
    Base.metadata.create_all(bind=engine)

    return TestClient(app)

def test_invalid_regime_api(client):
    response = client.post("/calculate-tax", json={
        "income": 500000,
        "hra": 0,
        "regime": "invalid"
    })

    assert response.status_code == 422

def test_negative_income(client):
    response = client.post("/calculate-tax", json={
        "income": -1000,
        "hra": 0,
        "regime": "old"
    })

    assert response.status_code == 422

def test_missing_field(client):
    response = client.post("/calculate-tax", json={
        "income": 500000,
        "regime": "old"
    })

    assert response.status_code == 422

def test_wrong_type(client):
    response = client.post("/calculate-tax", json={
        "income": "abc",
        "hra": 0,
        "regime": "old"
    })

    assert response.status_code == 422

def test_uppercase_regime(client):
    response = client.post("/calculate-tax", json={
        "income": 500000,
        "hra": 0,
        "regime": "OLD"
    })

    assert response.status_code == 422