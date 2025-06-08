import pytest
from app.core.haversine import calculate_distance
from app.services.geocode import get_coordinates
from app.services.address_cleaner import clean_addresses
from app.core.exceptions import AddressNotFoundError, GeocodingError

pytestmark = pytest.mark.asyncio

def test_haversine_calculation():
    """Test the Haversine distance calculation function."""
    # Toronto coordinates
    lat1, lon1 = 43.6532, -79.3832
    # Vancouver coordinates
    lat2, lon2 = 49.2827, -123.1207
    
    km_distance, mi_distance = calculate_distance(lat1, lon1, lat2, lon2)
    
    # The actual distance between Toronto and Vancouver is approximately 3,364 km
    assert isinstance(km_distance, float)
    assert isinstance(mi_distance, float)
    assert 3300 <= km_distance <= 3400  # km
    assert 2000 <= mi_distance <= 2200  # miles
    
async def test_geocoding_service(mock_nominatim_response):
    """Test the geocoding service with mock responses."""
    coords = await get_coordinates("Toronto, ON", "source")
    assert len(coords) == 2
    assert isinstance(coords[0], float)
    assert isinstance(coords[1], float)

async def test_geocoding_service_error():
    """Test geocoding service error handling."""
    with pytest.raises(AddressNotFoundError):
        await get_coordinates("NonexistentPlace12345", "source")

async def test_address_cleaning(mock_openai_response):
    """Test address cleaning service with mock responses."""
    result = await clean_addresses(
        "Tronto, ON",  # Misspelled
        "Vancover, BC"  # Misspelled
    )
    
    assert isinstance(result, dict)
    assert "source" in result
    assert "destination" in result
    assert "sourceCorrected" in result
    assert "destinationCorrected" in result 