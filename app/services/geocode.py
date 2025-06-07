from typing import Optional, Tuple
import httpx
from loguru import logger
from app.core.exceptions import GeocodingError, AddressNotFoundError
from app.core.config import settings


async def get_coordinates(address: str, side: str) -> Optional[Tuple[float, float]]:
    """
    Get coordinates (latitude, longitude) for an address using Nominatim.
    
    Args:
        address: The address to geocode
        
    Returns:
        Tuple of (latitude, longitude) if found, None otherwise
    """
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
    }
    
    headers = {
        "User-Agent": settings.NOMINATIM_USER_AGENT
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.NOMINATIM_BASE_URL}/search",
                params=params,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            
            results = response.json()
            
            if not results:
                logger.warning(f"No coordinates found for address: {address}")
                raise AddressNotFoundError(address, side)  
            return float(results[0]["lat"]), float(results[0]["lon"])
        
    except AddressNotFoundError:
        raise
            
    except Exception as e:
        logger.error(f"Error getting coordinates for {address}: {e}", exc_info=True)
        raise GeocodingError()