import requests
import os
import logging
from utils.cache_manager import CacheManager

cache = CacheManager()

def get_attractions(coords, travel_style='balanced', limit=10):
    """
    Get attractions and points of interest using OpenTripMap API
    """
    cache_key = f"attractions_{coords['lat']}_{coords['lon']}_{travel_style}_{limit}"

    # Check cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    try:
        api_key = os.getenv('OPENTRIPMAP_API_KEY')

        if not api_key:
            logging.warning("OpenTripMap API key not found, returning mock data")
            return get_mock_attractions(coords, travel_style, limit)

        # Get places within 5km radius
        url = "https://api.opentripmap.com/0.1/en/places/radius"
        params = {
            'radius': 5000,  # 5km
            'lon': coords['lon'],
            'lat': coords['lat'],
            'limit': limit,
            'apikey': api_key
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        places = response.json()

        # Filter and format attractions based on travel style
        attractions = []
        for place in places.get('features', []):
            properties = place.get('properties', {})
            if properties.get('name'):
                attraction = {
                    'name': properties['name'],
                    'kinds': properties.get('kinds', '').split(','),
                    'rate': properties.get('rate', 0),
                    'distance': place.get('properties', {}).get('dist', 0),
                    'osm_id': properties.get('osm_id')
                }

                # Filter based on travel style
                if should_include_attraction(attraction, travel_style):
                    attractions.append(attraction)

        # Cache and return
        cache.set(cache_key, attractions[:limit])
        return attractions[:limit]

    except Exception as e:
        logging.error(f"Error fetching attractions: {str(e)}")
        return get_mock_attractions(coords, travel_style, limit)

def should_include_attraction(attraction, travel_style):
    """
    Filter attractions based on travel style
    """
    kinds = attraction.get('kinds', [])

    style_filters = {
        'relaxed': ['museums', 'parks', 'beaches', 'churches', 'historic'],
        'adventure': ['mountains', 'hiking', 'sports', 'natural', 'geological'],
        'family': ['museums', 'zoos', 'aquariums', 'parks', 'amusement_parks'],
        'luxury': ['museums', 'historic', 'architecture', 'galleries', 'theatres']
    }

    relevant_kinds = style_filters.get(travel_style, [])
    return any(kind in ' '.join(kinds) for kind in relevant_kinds)

def get_mock_attractions(coords, travel_style, limit):
    """
    Return mock attraction data for testing
    """
    mock_attractions = [
        {'name': 'Central Park', 'kinds': ['parks'], 'rate': 4.5, 'distance': 500},
        {'name': 'City Museum', 'kinds': ['museums'], 'rate': 4.2, 'distance': 800},
        {'name': 'Historic Cathedral', 'kinds': ['churches', 'historic'], 'rate': 4.0, 'distance': 1200},
        {'name': 'Local Market', 'kinds': ['markets'], 'rate': 4.3, 'distance': 600},
        {'name': 'Scenic Viewpoint', 'kinds': ['natural'], 'rate': 4.1, 'distance': 1500},
        {'name': 'Art Gallery', 'kinds': ['galleries'], 'rate': 3.8, 'distance': 900},
        {'name': 'Botanical Garden', 'kinds': ['parks'], 'rate': 4.4, 'distance': 1100},
        {'name': 'Aquarium', 'kinds': ['aquariums'], 'rate': 4.6, 'distance': 1400}
    ]

    # Filter based on style - ensure we have some matches for 'balanced'
    if travel_style == 'balanced':
        # For balanced, include a mix of parks, museums, historic sites
        filtered = [attr for attr in mock_attractions if any(kind in attr['kinds'] for kind in ['parks', 'museums', 'historic', 'churches'])]
    else:
        filtered = [attr for attr in mock_attractions if should_include_attraction(attr, travel_style)]

    return filtered[:limit]
