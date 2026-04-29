from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from functools import lru_cache
from app.config.env_config import get_settings

@lru_cache
def get_engine():
    settings = get_settings()
    return create_engine(
        settings.DB_URL,
        connect_args={'check_same_thread': False}
    )

engine = get_engine()

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
