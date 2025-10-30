import requests
import os
import logging
from utils.cache_manager import CacheManager

cache = CacheManager()

def search_hotels(coords, checkin_date, checkout_date, travelers=1, budget=1000):
    """
    Search for hotels using Skyscanner API or fallback to open data
    """
    cache_key = f"hotels_{coords['lat']}_{coords['lon']}_{checkin_date}_{checkout_date}_{travelers}_{budget}"

    # Check cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    try:
        api_key = os.getenv('SKYSCANNER_API_KEY')

        if not api_key:
            logging.warning("Skyscanner API key not found, returning mock data")
            return get_mock_hotels(coords, checkin_date, checkout_date, travelers, budget)

        # Placeholder for real API call
        # Real implementation would use Skyscanner Hotels API

        # For now, return mock data
        hotels = get_mock_hotels(coords, checkin_date, checkout_date, travelers, budget)
        cache.set(cache_key, hotels)
        return hotels

    except Exception as e:
        logging.error(f"Error searching hotels: {str(e)}")
        return get_mock_hotels(coords, checkin_date, checkout_date, travelers, budget)

def get_mock_hotels(coords, checkin_date, checkout_date, travelers, budget):
    """
    Return mock hotel data for testing
    """
    # Calculate number of nights
    from datetime import datetime
    checkin = datetime.fromisoformat(checkin_date)
    checkout = datetime.fromisoformat(checkout_date)
    nights = (checkout - checkin).days

    return [
        {
            'name': 'Budget Inn',
            'rating': 3.5,
            'price_per_night': min(80, budget // (nights * 2)),
            'total_price': min(80 * nights, budget // 2),
            'amenities': ['WiFi', 'Breakfast'],
            'category': 'economy'
        },
        {
            'name': 'Comfort Hotel',
            'rating': 4.2,
            'price_per_night': min(120, budget // nights),
            'total_price': min(120 * nights, budget),
            'amenities': ['WiFi', 'Breakfast', 'Pool', 'Gym'],
            'category': 'balanced'
        },
        {
            'name': 'Luxury Resort',
            'rating': 4.8,
            'price_per_night': min(200, budget // nights),
            'total_price': min(200 * nights, budget),
            'amenities': ['WiFi', 'Breakfast', 'Pool', 'Spa', 'Restaurant'],
            'category': 'premium'
        }
    ]
