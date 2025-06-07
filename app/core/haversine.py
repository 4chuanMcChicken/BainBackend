from math import radians, sin, cos, sqrt, atan2
from typing import Tuple


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> Tuple[float, float]:
    """
    Calculate the great circle distance between two points on Earth
    using the haversine formula.
    
    Args:
        lat1: Latitude of point 1 in degrees
        lon1: Longitude of point 1 in degrees
        lat2: Latitude of point 2 in degrees
        lon2: Longitude of point 2 in degrees
        
    Returns:
        Tuple of (distance in kilometers, distance in miles)
    """
    # Earth's radius in kilometers
    R = 6371.0

    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Calculate distances
    distance_km = round(R * c, 2)
    distance_miles = round(distance_km * 0.621371, 2)

    return distance_km, distance_miles 