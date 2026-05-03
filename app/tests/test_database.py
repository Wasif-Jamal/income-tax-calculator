from sqlalchemy import text
from app.config.db_config import get_engine

def test_database_connection(monkeypatch):
    monkeypatch.setenv('DB_URL', "sqlite:///./test.db")
    get_engine.cache_clear()
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
        assert result.scalar() == 1