from sqlalchemy import text
from app.db.database import engine

def test_database_connection(monkeypatch):
    monkeypatch.setenv('DB_URL', "sqlite:///./test.db")
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
        assert result.scalar() == 1