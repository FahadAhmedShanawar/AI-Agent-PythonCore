# Event Planner Agent Design Document

## Overview

The Event Planner Agent is a comprehensive web application for organizing events, built with Python Flask and supporting services for venue discovery, RSVP management, and to-do generation.

## Architecture

### Core Components

- **Flask Web App**: Handles HTTP requests, serves UI templates, provides REST API endpoints
- **Services Layer**:
  - VenueFinder: Integrates Eventbrite API with OSM fallback
  - RSVPManager: Manages attendee data with Google Sheets sync
  - TodoGenerator: Creates dynamic checklists based on event type
- **Utilities**: GeocodeUtil for location services
- **Data Layer**: CSV files for local persistence, Google Sheets for live collaboration

### Data Flow

1. User creates event via web form
2. Event data stored in events.csv
3. Venue finder queries APIs, returns top 5 matches
4. RSVPs managed with CRUD operations, synced to Google Sheets
5. To-do lists generated dynamically, exportable in multiple formats

## API Integrations

### Eventbrite API
- Endpoint: `https://www.eventbriteapi.com/v3/events/search/`
- Parameters: location, price range, capacity
- Fallback: OSM-based venue suggestions

### Google Sheets API
- Service Account Authentication
- Real-time sync of RSVP data
- CSV backup for offline access

### Nominatim Geocoding
- User Agent: "event_planner_agent"
- Caching: In-memory cache to reduce API calls
- Rate Limiting: Built-in delays between requests

### SMTP Email
- Providers: Gmail (app password), other SMTP servers
- Purpose: RSVP confirmations and reminders

## Security Considerations

- API keys stored in .env, never committed
- Input sanitization on all user data
- OAuth validation for Google Sheets access
- Exponential backoff for external API calls
- Logging of user actions and API interactions

## Deployment Strategy

### Free Hosting Options
- **Railway**: Git-based deploys, PostgreSQL free tier
- **Render**: Web service with free tier, auto-deploys from Git
- **Vercel**: Serverless functions, suitable for lightweight apps

### Environment Variables
- EVENTBRITE_API_KEY
- GOOGLE_SHEETS_CREDENTIALS_FILE
- GOOGLE_SHEETS_SPREADSHEET_ID
- SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
- LOG_LEVEL, SECRET_KEY

## Testing Strategy

### Unit Tests
- VenueFinder: API integration and fallback logic
- RSVPManager: CRUD operations and sync
- TodoGenerator: Checklist generation by event type
- GeocodeUtil: Location services

### Integration Tests
- End-to-end flows: Create event → Find venues → Add RSVPs → Generate to-dos → Export

### Manual Testing Scenarios
- Birthday party (small budget, 30 guests)
- Corporate conference (large capacity, AV needs)
- Outdoor meetup (weather contingency)

## UI/UX Design

### Web Interface
- Simple forms for event creation
- List/calendar view for events
- Venue suggestions panel
- RSVP dashboard with filters
- To-do manager with drag-and-drop ordering

### API Endpoints
- `/api/events`: POST to create events
- `/api/venues`: GET venue suggestions
- `/api/rsvps/<event_id>`: CRUD for RSVPs
- `/api/todos/<event_id>`: GET to-do lists
- `/export/todos/<event_id>/<format>`: Export functionality

## Future Enhancements

- Calendar integration (Google Calendar, Outlook)
- Payment processing for venue bookings
- Mobile app companion
- AI-powered event recommendations
- Multi-language support
