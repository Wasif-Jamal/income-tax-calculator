from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.pool import StaticPool
from functools import lru_cache
from app.config.env_config import get_settings

@lru_cache
def get_engine():
    settings = get_settings()
    if "sqlite" in settings.DB_URL:
        return create_engine(
            settings.DB_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )

    return create_engine(settings.DB_URL)

engine = get_engine()

def get_session_local():
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine()
    )

Base = declarative_base()

def get_db():
    """Provide a database session.

    Yields:
        Session: SQLAlchemy session instance.

    Ensures:
        Session is properly closed after use.
    """
    SessionLocal = get_session_local()
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
