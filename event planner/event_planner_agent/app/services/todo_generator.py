import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class TodoGenerator:
    def generate_todos(self, event):
        event_type = event['event_type']
        event_date = datetime.fromisoformat(event['date'])
        todos = []

        # Base todos by event type
        if event_type == 'birthday':
            todos.extend(self._birthday_todos(event_date))
        elif event_type == 'conference':
            todos.extend(self._conference_todos(event_date))
        elif event_type == 'meetup':
            todos.extend(self._meetup_todos(event_date))
        elif event_type == 'wedding':
            todos.extend(self._wedding_todos(event_date))
        else:
            todos.extend(self._generic_todos(event_date))

        # Add common todos
        todos.extend(self._common_todos(event_date))

        # Sort by deadline and priority
        todos.sort(key=lambda x: (x['deadline'], -x['priority']))

        return todos

    def _birthday_todos(self, event_date):
        return [
            {'task': 'Order birthday cake', 'deadline': (event_date - timedelta(days=7)).isoformat(), 'priority': 8, 'owner': 'user', 'category': '1 week'},
            {'task': 'Send invitations', 'deadline': (event_date - timedelta(days=14)).isoformat(), 'priority': 7, 'owner': 'user', 'category': '1 month'},
            {'task': 'Plan games/activities', 'deadline': (event_date - timedelta(days=3)).isoformat(), 'priority': 6, 'owner': 'user', 'category': 'Day-of'},
            {'task': 'Buy decorations', 'deadline': (event_date - timedelta(days=7)).isoformat(), 'priority': 5, 'owner': 'user', 'category': '1 week'}
        ]

    def _conference_todos(self, event_date):
        return [
            {'task': 'Book AV equipment', 'deadline': (event_date - timedelta(days=30)).isoformat(), 'priority': 9, 'owner': 'vendor', 'category': '1 month'},
            {'task': 'Arrange catering', 'deadline': (event_date - timedelta(days=14)).isoformat(), 'priority': 8, 'owner': 'vendor', 'category': '1 month'},
            {'task': 'Prepare speaker materials', 'deadline': (event_date - timedelta(days=7)).isoformat(), 'priority': 7, 'owner': 'user', 'category': '1 week'},
            {'task': 'Set up registration desk', 'deadline': event_date.isoformat(), 'priority': 6, 'owner': 'user', 'category': 'Day-of'}
        ]

    def _meetup_todos(self, event_date):
        return [
            {'task': 'Check weather forecast', 'deadline': (event_date - timedelta(days=1)).isoformat(), 'priority': 7, 'owner': 'user', 'category': 'Day-of'},
            {'task': 'Arrange backup indoor venue', 'deadline': (event_date - timedelta(days=7)).isoformat(), 'priority': 6, 'owner': 'user', 'category': '1 week'},
            {'task': 'Prepare agenda/topics', 'deadline': (event_date - timedelta(days=14)).isoformat(), 'priority': 5, 'owner': 'user', 'category': '1 month'},
            {'task': 'Promote on social media', 'deadline': (event_date - timedelta(days=21)).isoformat(), 'priority': 4, 'owner': 'user', 'category': '1 month'}
        ]

    def _wedding_todos(self, event_date):
        return [
            {'task': 'Book photographer/videographer', 'deadline': (event_date - timedelta(days=60)).isoformat(), 'priority': 10, 'owner': 'vendor', 'category': '1 month'},
            {'task': 'Send save-the-dates', 'deadline': (event_date - timedelta(days=90)).isoformat(), 'priority': 9, 'owner': 'user', 'category': '1 month'},
            {'task': 'Choose menu with caterer', 'deadline': (event_date - timedelta(days=30)).isoformat(), 'priority': 8, 'owner': 'vendor', 'category': '1 month'},
            {'task': 'Finalize guest list', 'deadline': (event_date - timedelta(days=14)).isoformat(), 'priority': 7, 'owner': 'user', 'category': '1 week'}
        ]

    def _generic_todos(self, event_date):
        return [
            {'task': 'Confirm venue booking', 'deadline': (event_date - timedelta(days=30)).isoformat(), 'priority': 8, 'owner': 'user', 'category': '1 month'},
            {'task': 'Send invitations', 'deadline': (event_date - timedelta(days=14)).isoformat(), 'priority': 7, 'owner': 'user', 'category': '1 month'},
            {'task': 'Arrange transportation', 'deadline': (event_date - timedelta(days=7)).isoformat(), 'priority': 6, 'owner': 'user', 'category': '1 week'},
            {'task': 'Prepare welcome speech', 'deadline': (event_date - timedelta(days=1)).isoformat(), 'priority': 5, 'owner': 'user', 'category': 'Day-of'}
        ]

    def _common_todos(self, event_date):
        return [
            {'task': 'Create event budget', 'deadline': (event_date - timedelta(days=60)).isoformat(), 'priority': 9, 'owner': 'user', 'category': '1 month'},
            {'task': 'Purchase insurance', 'deadline': (event_date - timedelta(days=30)).isoformat(), 'priority': 8, 'owner': 'user', 'category': '1 month'},
            {'task': 'Set up event website/page', 'deadline': (event_date - timedelta(days=21)).isoformat(), 'priority': 6, 'owner': 'user', 'category': '1 month'},
            {'task': 'Test all equipment', 'deadline': event_date.isoformat(), 'priority': 7, 'owner': 'user', 'category': 'Day-of'}
        ]
