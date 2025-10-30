import pytest
import pandas as pd
from app.services.venue_finder import VenueFinder
from app.services.rsvp_manager import RSVPManager
from app.services.todo_generator import TodoGenerator
from app.utils.geocode import GeocodeUtil

class TestVenueFinder:
    def test_find_venues_fallback(self):
        finder = VenueFinder()
        venues = finder.find_venues("New York", 1000, 50)
        assert len(venues) <= 5
        assert all('name' in v for v in venues)
        assert all('rationale' in v for v in venues)

class TestRSVPManager:
    def test_add_rsvp(self):
        manager = RSVPManager()
        rsvp_data = {'name': 'Test User', 'email': 'test@example.com', 'status': 'attending'}
        manager.add_rsvp(1, rsvp_data)
        rsvps = manager.get_rsvps(1)
        assert len(rsvps) > 0
        assert any(r['name'] == 'Test User' for r in rsvps)

class TestTodoGenerator:
    def test_generate_birthday_todos(self):
        generator = TodoGenerator()
        event = {'event_type': 'birthday', 'date': '2023-12-25'}
        todos = generator.generate_todos(event)
        assert len(todos) > 0
        assert all('task' in t for t in todos)
        assert all('deadline' in t for t in todos)

class TestGeocodeUtil:
    def test_geocode(self):
        util = GeocodeUtil()
        coords = util.geocode("New York")
        assert isinstance(coords, tuple)
        assert len(coords) == 2
