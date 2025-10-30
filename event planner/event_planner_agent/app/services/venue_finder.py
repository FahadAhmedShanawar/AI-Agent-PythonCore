import requests
import os
import logging
from utils.geocode import GeocodeUtil
import time

logger = logging.getLogger(__name__)

class VenueFinder:
    def __init__(self):
        self.eventbrite_key = os.getenv('EVENTBRITE_API_KEY')
        self.geocode_util = GeocodeUtil()

    def find_venues(self, location, budget, attendees):
        try:
            # Try Eventbrite API first
            venues = self._find_via_eventbrite(location, budget, attendees)
            if venues:
                return venues
        except Exception as e:
            logger.warning(f"Eventbrite API failed: {e}. Falling back to OSM.")

        # Fallback to OSM
        return self._find_via_osm(location, budget, attendees)

    def _find_via_eventbrite(self, location, budget, attendees):
        url = "https://www.eventbriteapi.com/v3/events/search/"
        params = {
            'location.address': location,
            'price': f'0-{budget}',
            'capacity': attendees,
            'expand': 'venue'
        }
        headers = {'Authorization': f'Bearer {self.eventbrite_key}'}

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        venues = []
        for event in data.get('events', [])[:5]:
            venue = event.get('venue', {})
            venues.append({
                'name': venue.get('name', 'Unknown'),
                'address': venue.get('address', {}).get('localized_address_display', ''),
                'capacity': event.get('capacity', 0),
                'price': 'Within budget',
                'rationale': f"Capacity matches attendees, within budget. Distance: {self._calculate_distance(location, venue.get('address', {}).get('latitude'), venue.get('address', {}).get('longitude'))} km",
                'contact': venue.get('address', {}).get('localized_address_display', ''),
                'link': event.get('url', '')
            })
        return venues

    def _find_via_osm(self, location, budget, attendees):
        # Use OSM Nominatim for venue search (simplified)
        lat, lon = self.geocode_util.geocode(location)
        # Query for places like 'venue', 'hall', etc. (mock implementation)
        # In real implementation, use Overpass API or similar
        mock_venues = [
            {'name': 'Local Community Hall', 'lat': lat + 0.01, 'lon': lon + 0.01, 'capacity': 100, 'price_range': 'Low'},
            {'name': 'Downtown Conference Center', 'lat': lat - 0.01, 'lon': lon - 0.01, 'capacity': 200, 'price_range': 'Medium'},
            {'name': 'Riverside Park Pavilion', 'lat': lat + 0.02, 'lon': lon + 0.02, 'capacity': 50, 'price_range': 'Low'},
            {'name': 'City Ballroom', 'lat': lat - 0.02, 'lon': lon - 0.02, 'capacity': 150, 'price_range': 'High'},
            {'name': 'Neighborhood Club', 'lat': lat + 0.005, 'lon': lon + 0.005, 'capacity': 80, 'price_range': 'Medium'}
        ]

        venues = []
        for v in mock_venues:
            if v['capacity'] >= attendees:
                distance = self._calculate_distance(location, v['lat'], v['lon'])
                rationale = f"Capacity sufficient, {v['price_range']} price range. Distance: {distance:.2f} km"
                venues.append({
                    'name': v['name'],
                    'address': f"Approx {distance:.2f} km from {location}",
                    'capacity': v['capacity'],
                    'price': v['price_range'],
                    'rationale': rationale,
                    'contact': 'Contact local directory',
                    'link': ''
                })
        return sorted(venues, key=lambda x: self._score_venue(x, budget, attendees))[:5]

    def _calculate_distance(self, location, lat2, lon2):
        lat1, lon1 = self.geocode_util.geocode(location)
        # Haversine formula (simplified)
        from math import radians, cos, sin, asin, sqrt
        dlon = radians(lon2) - radians(lon1)
        dlat = radians(lat2) - radians(lat1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r

    def _score_venue(self, venue, budget, attendees):
        # Simple scoring: lower distance, capacity match, price fit
        score = 0
        if venue['capacity'] >= attendees:
            score += 10
        if 'Low' in venue['price'] or 'Medium' in venue['price']:
            score += 5
        # Distance score (lower distance better)
        distance = float(venue['rationale'].split('Distance: ')[1].split(' km')[0])
        score -= distance
        return -score  # Higher score first
