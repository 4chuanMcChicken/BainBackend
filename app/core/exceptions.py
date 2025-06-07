from typing import Any, Dict, Optional
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str


class APIError(HTTPException):
    """Base API exception with structured detail"""
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail={"code": code, "message": message}
        )


def format_validation_error(exc: RequestValidationError) -> Dict[str, Any]:
    """Format validation errors into our standard error format"""
    return {
        "code": "VALIDATION_ERROR",
        "message": "Request validation failed"
    }


def format_error_response(status_code: int, exc: Exception) -> Dict[str, Any]:
    """Format any exception into our standard error format"""
    if isinstance(exc, HTTPException):
        # If it's already an HTTPException, check if detail is properly structured
        if isinstance(exc.detail, dict) and "code" in exc.detail and "message" in exc.detail:
            return exc.detail
        # If detail is a string, convert to our format
        return {
            "code": "HTTP_ERROR",
            "message": str(exc.detail)
        }
    
    # For any other exception, provide a generic error
    return {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "An internal server error occurred"
    }


class GeocodingError(APIError):
    def __init__(self):
        super().__init__(
            status_code=502,  # Bad Gateway – upstream service error
            code="GEOCODING_PROVIDER_ERROR",
            message="The geocoding service is currently unavailable. Please try again later."
        )


class AddressNotFoundError(APIError):
    def __init__(self, address: str, side: str):
        super().__init__(
         status_code=422,
            code="ADDRESS_NOT_FOUND",
            message=f"Could not find coordinates for {side} address: {address}"   
        )