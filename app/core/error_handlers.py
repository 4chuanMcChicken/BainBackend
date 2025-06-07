from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from app.core.exceptions import format_error_response, format_validation_error

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(
        f"HTTP {exc.status_code} error during {request.method} {request.url.path}: {exc.detail}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": format_error_response(exc.status_code, exc)}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        f"Validation error during {request.method} {request.url.path}: {exc.errors()}"
    )
    return JSONResponse(
        status_code=422,
        content={"detail": format_validation_error(exc)}
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(
        f"Database error during {request.method} {request.url.path}",
        exc_info=exc
    )
    return JSONResponse(
        status_code=500,
        content={"detail": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An internal error occurred. Please try again later."
        }}
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled exception during {request.method} {request.url.path}",
        exc_info=exc
    )
    return JSONResponse(
        status_code=500,
        content={"detail": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An internal error occurred. Please try again later."
        }}
    )
