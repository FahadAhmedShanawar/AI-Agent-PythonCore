import requests
import logging
from utils.cache_manager import CacheManager

cache = CacheManager()

def get_coordinates(destination):
    """
    Get latitude and longitude for a destination using Nominatim API
    """
    cache_key = f"geocode_{destination.lower().replace(' ', '_')}"

    # Check cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': destination,
            'format': 'json',
            'limit': 1
        }

        response = requests.get(url, params=params, headers={'User-Agent': 'VirtualTravelAgent/1.0'})
        response.raise_for_status()

        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            result = {'lat': lat, 'lon': lon}

            # Cache the result
            cache.set(cache_key, result)
            return result

    except Exception as e:
        logging.error(f"Error geocoding {destination}: {str(e)}")

    return None
