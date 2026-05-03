import pytest
from fastapi.testclient import TestClient
from app.config.db_config import Base, get_engine

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("DB_URL", "sqlite:///:memory:")
    get_engine.cache_clear()

    from app.main import app

    engine = get_engine()
    Base.metadata.create_all(bind=engine)

    return TestClient(app)

def test_calculate_tax(client):
    response = client.post('/calculate-tax', json={
        'income': 1000000,
        'hra': 200000,
        'regime': 'old'
    })

    assert response.status_code == 200
    data = response.json()
    print(data)

    assert 'tax' in data

def test_get_history(client):
    client.post("/calculate-tax", json={
        "income": 500000,
        "hra": 100000,
        "regime": "new"
    })

    response = client.get("/history")

    assert response.status_code == 200
    data = response.json()
    print(data)

    assert isinstance(data, list)
    assert len(data) >= 1
    assert "income" in data[0]