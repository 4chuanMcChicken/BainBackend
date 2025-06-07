# app/services/exceptions.py
from fastapi import HTTPException

class GeocodingError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=502,  # Bad Gateway – upstream service error
            detail={
                "code": "GEOCODING_PROVIDER_ERROR",
                "message": "The geocoding service is currently unavailable. Please try again later."
            }
        )

class AddressNotFoundError(HTTPException):
    def __init__(self, address: str, side: str):
        super().__init__(
            status_code=422,
            detail={
                "code": "ADDRESS_NOT_FOUND",
                "message": f"Could not find coordinates for {side} address: {address}"
            }
        )
