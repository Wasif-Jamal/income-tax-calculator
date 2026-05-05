from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import AppError
from app.config.log_config import logger


async def app_error_handler(request: Request, exc: AppError):
    logger.error(f"AppError: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
