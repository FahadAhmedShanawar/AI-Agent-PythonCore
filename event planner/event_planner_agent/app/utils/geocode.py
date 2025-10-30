from geopy.geocoders import Nominatim
import time
import logging

logger = logging.getLogger(__name__)

class GeocodeUtil:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="event_planner_agent")
        self.cache = {}  # Simple in-memory cache

    def geocode(self, location):
        if location in self.cache:
            return self.cache[location]

        try:
            location_obj = self.geolocator.geocode(location)
            if location_obj:
                coords = (location_obj.latitude, location_obj.longitude)
                self.cache[location] = coords
                return coords
            else:
                logger.warning(f"Could not geocode: {location}")
                return (0, 0)  # Default fallback
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            return (0, 0)

    def reverse_geocode(self, lat, lon):
        try:
            location_obj = self.geolocator.reverse((lat, lon))
            return location_obj.address if location_obj else "Unknown location"
        except Exception as e:
            logger.error(f"Reverse geocoding error: {e}")
            return "Unknown location"
