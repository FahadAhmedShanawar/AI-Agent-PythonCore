# Event Planner Agent

An AI-powered event planning assistant that helps organize events, find venues, manage RSVPs, and generate dynamic to-do lists.

## Features

- **Event Input & Validation**: Create events with date, time, location, attendees, type, budget, and requirements
- **Venue Finder**: Discover top 5 venues using Eventbrite API or OSM fallback, scored by distance, capacity, and budget
- **RSVP Manager**: CRUD operations for attendees, Google Sheets sync, email confirmations
- **Dynamic To-Do Generator**: Prioritized checklists based on event type with deadlines and owners
- **Export Options**: CSV, JSON, PDF export for to-do lists
- **Web UI**: Simple Flask-based interface for all operations

## Setup

### Prerequisites
- Python 3.10+
- Virtual environment (venv)

### Installation

1. Clone or download the project
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### API Keys Setup

1. **Eventbrite API**: Sign up at [Eventbrite Developer](https://www.eventbrite.com/platform/api/), get API key
2. **Google Sheets API**: Create service account, enable Sheets API, share spreadsheet with service account email
3. **Email SMTP**: Use Gmail with app password or other SMTP provider

Create `.env` file from `.env.example` and fill in your keys:

```bash
cp .env.example .env
# Edit .env with your API keys
```

### Running Locally

```bash
python -m app.main
```

Or use the script:
```bash
./scripts/run_local.sh
```

Visit `http://localhost:5000` to access the web interface.

## Usage

1. **Create Event**: Fill form with event details
2. **Find Venues**: View top 5 suggestions with rationales
3. **Manage RSVPs**: Add/update attendee responses, syncs to Google Sheets
4. **Generate To-Dos**: Get prioritized checklist based on event type
5. **Export**: Download to-do lists in CSV/JSON/PDF

## Testing

Run unit tests:
```bash
pytest tests/test_services.py
```

## Deployment

See `deploy/README.md` for hosting options (Railway, Render, Vercel).

## Architecture

- **Flask App**: Web framework for UI and API
- **Services**: Modular components for venue finding, RSVP management, to-do generation
- **Data Persistence**: CSV for local storage, Google Sheets for live sync
- **APIs**: Eventbrite for venues, Nominatim for geocoding, SMTP for emails

## Contributing

1. Fork the repo
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## License

MIT License

"Just completed my Event Planner Agent! Organize events, manage RSVPs, and create to-do lists effortlessly. #rehancodingwithai #codingwithai"
