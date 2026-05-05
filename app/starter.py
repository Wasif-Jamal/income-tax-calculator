from fastapi import FastAPI

from app.config.db_config import Base, engine
from app.routes.tax import router as tax_router
from app.config.log_config import logger
from app.exceptions.handlers import app_error_handler, global_exception_handler
from app.exceptions.custom_exceptions import AppError

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

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    return app