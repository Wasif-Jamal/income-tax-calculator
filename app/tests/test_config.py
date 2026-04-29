import pytest
from app.config.env_config import Settings

def test_db_url_missing(monkeypatch):
    monkeypatch.delenv("DB_URL", raising=False)

    with pytest.raises(ValueError):
        Settings()