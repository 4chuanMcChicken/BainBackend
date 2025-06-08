from typing import Dict
import httpx
from loguru import logger

from app.core.config import settings
from app.core.exceptions import APIError


class RecaptchaVerificationError(APIError):
    def __init__(self):
        super().__init__(
            status_code=400,
            code="INVALID_RECAPTCHA",
            message="reCAPTCHA verification failed. Please try again."
        )


async def verify_recaptcha(token: str) -> None:
    """
    Verify reCAPTCHA token with Google's API
    
    Args:
        token: The reCAPTCHA response token from the client
        
    Raises:
        RecaptchaVerificationError: If verification fails
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": settings.RECAPTCHA_SECRET_KEY,
                    "response": token
                },
                timeout=5.0
            )
            
            response.raise_for_status()
            result = response.json()
            
            if not result.get("success", False):
                logger.warning(f"reCAPTCHA verification failed: {result}")
                raise RecaptchaVerificationError()
                
            logger.debug("reCAPTCHA verification successful")
            
    except httpx.HTTPError as e:
        logger.error(f"Error verifying reCAPTCHA: {str(e)}")
        raise RecaptchaVerificationError()
    except Exception as e:
        logger.error(f"Unexpected error during reCAPTCHA verification: {str(e)}")
        raise RecaptchaVerificationError() 