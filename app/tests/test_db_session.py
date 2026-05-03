from sqlalchemy import text
from app.config.db_config import get_db, get_engine

def test_get_db(monkeypatch):
    monkeypatch.setenv('DB_URL', 'sqlite:///./test.db')

    # clear cached engine so new DB is used
    get_engine.cache_clear()

    # create generator
    db_gen = get_db()

    # get session
    db = next(db_gen)

    # check connection is active
    conn = db.connection()
    assert not conn.closed

    # test session works
    result = db.execute(text("SELECT 1"))
    assert result.scalar() == 1

    # close session (trigger finally block)
    try:
        next(db_gen)
    except StopIteration:
        pass
    # check connection is closed
    assert conn.closed