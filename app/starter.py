from fastapi import FastAPI

from app.config.db_config import Base, engine
from app.routes.tax import router as tax_router
from app.config.log_config import logger

logger.info("Starting application...")

def start_application() -> FastAPI:
    app = FastAPI(
        title="Income Tax Calculator",
        version="1.0.0",
        description="Simple tax calculator API"
    )

    # DB init
    Base.metadata.create_all(bind=engine)

    # Routes
    app.include_router(tax_router)

    return app