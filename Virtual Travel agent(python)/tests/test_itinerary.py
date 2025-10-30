import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import geocoding, flights_service, hotels_service, attractions_service
from utils import cost_estimator, cache_manager

class TestVirtualTravelAgent(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.coords = {'lat': 40.7128, 'lon': -74.0060}  # New York
        self.destination = "New York"
        self.start_date = "2024-06-01"
        self.end_date = "2024-06-05"
        self.travelers = 2
        self.budget = 2000

    @patch('services.geocoding.requests.get')
    def test_geocoding_success(self, mock_get):
        """Test successful geocoding"""
        mock_response = MagicMock()
        mock_response.json.return_value = [{'lat': '40.7128', 'lon': '-74.0060'}]
        mock_get.return_value = mock_response

        result = geocoding.get_coordinates("New York")
        self.assertIsNotNone(result)
        self.assertEqual(result['lat'], 40.7128)
        self.assertEqual(result['lon'], -74.0060)

    def test_geocoding_failure(self):
        """Test geocoding failure"""
        result = geocoding.get_coordinates("NonexistentPlace12345")
        self.assertIsNone(result)

    def test_flights_mock_data(self):
        """Test flight service returns mock data"""
        flights = flights_service.get_mock_flights(
            self.destination, self.start_date, self.end_date, self.travelers
        )
        self.assertIsInstance(flights, list)
        self.assertGreater(len(flights), 0)
        self.assertIn('price', flights[0])

    def test_hotels_mock_data(self):
        """Test hotel service returns mock data"""
        hotels = hotels_service.get_mock_hotels(
            self.coords, self.start_date, self.end_date, self.travelers, self.budget
        )
        self.assertIsInstance(hotels, list)
        self.assertGreater(len(hotels), 0)
        self.assertIn('price_per_night', hotels[0])

    def test_attractions_mock_data(self):
        """Test attractions service returns mock data"""
        attractions = attractions_service.get_mock_attractions(
            self.coords, 'balanced', 5
        )
        self.assertIsInstance(attractions, list)
        self.assertGreater(len(attractions), 0)
        self.assertIn('name', attractions[0])

    def test_cost_calculation(self):
        """Test cost estimation"""
        mock_itinerary = {
            'days': [{'day': 1}, {'day': 2}, {'day': 3}, {'day': 4}]
        }

        costs = cost_estimator.calculate_total_cost(mock_itinerary, self.travelers)
        self.assertIsInstance(costs, dict)
        self.assertIn('total', costs)
        self.assertIn('per_person', costs)
        self.assertGreater(costs['total'], 0)

    def test_cache_manager(self):
        """Test cache functionality"""
        import tempfile
        import os

        # Use temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
            db_path = tmp.name

        cache = None
        try:
            cache = cache_manager.CacheManager(db_path)

            # Test set and get
            cache.set('test_key', {'data': 'test_value'})
            result = cache.get('test_key')
            self.assertIsNotNone(result)
            self.assertEqual(result['data'], 'test_value')

            # Test non-existent key
            result = cache.get('non_existent_key')
            self.assertIsNone(result)
        finally:
            # Clean up - close connection first if cache exists
            if cache:
                # Force close any open connections
                import sqlite3
                try:
                    conn = sqlite3.connect(db_path)
                    conn.close()
                except:
                    pass
            if os.path.exists(db_path):
                try:
                    os.unlink(db_path)
                except PermissionError:
                    pass  # Ignore if can't delete

    def test_budget_validation(self):
        """Test budget validation"""
        total_cost = 1500
        budget = 2000
        travelers = 2

        is_valid = cost_estimator.validate_budget(total_cost, budget, travelers)
        self.assertTrue(is_valid)

        # Test over budget - budget is per person, so 3000 > 2000 * 2 = 4000, but wait, no:
        # The function now checks total_cost <= budget, so 3000 <= 2000 should be False
        is_valid_over = cost_estimator.validate_budget(3000, budget, travelers)
        self.assertFalse(is_valid_over)

if __name__ == '__main__':
    unittest.main()
