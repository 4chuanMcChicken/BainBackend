from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import access_log_middleware
from app.api import health, distance, history


# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add access logging middleware
app.middleware("http")(access_log_middleware)

# Global error handler for database errors
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Global handler for database errors"""
    logger.error(
        f"Database error occurred during {request.method} {request.url.path}",
        exc_info=exc
    )
    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An internal error occurred. Please try again later."
        }
    )

# Include routers
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(distance.router, prefix=settings.API_V1_STR)
app.include_router(history.router, prefix=settings.API_V1_STR) 