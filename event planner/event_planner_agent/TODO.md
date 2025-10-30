# Event Planner Agent Development TODO

## 1. Project Setup
- [x] Create directory structure (/event_planner_agent with all subdirs)
- [x] Set up virtual environment
- [x] Create requirements.txt with dependencies (Flask, pandas, requests, geopy, gspread, oauth2client, smtplib, reportlab, fpdf, pytest, pytest-cov)

## 2. Core Application Structure
- [x] Create app/__init__.py
- [x] Implement app/main.py (Flask app entry)
- [x] Create app/routes.py (HTTP endpoints and UI handlers)
- [x] Create app/models/__init__.py

## 3. Services Implementation
- [x] Implement app/services/venue_finder.py (Eventbrite API integration, fallback to OSM)
- [x] Implement app/services/rsvp_manager.py (CRUD for RSVPs, Google Sheets sync, CSV backup)
- [x] Implement app/services/todo_generator.py (Dynamic to-do lists with priorities and deadlines)

## 4. Utilities and Data
- [x] Create app/utils/geocode.py (Nominatim/Geopy for geocoding)
- [x] Create data/events.csv (sample event store)
- [x] Create data/rsvps.csv (RSVP backup)
- [x] Create data/sample_events.csv (for testing)

## 5. Configuration and Security
- [x] Create .env.example (API keys, secrets)
- [x] Implement logging to logs/app.log
- [x] Add error handling, input sanitization, OAuth validation, exponential backoff

## 6. Testing
- [x] Create tests/test_services.py (unit tests for venue_finder, rsvp_manager, and todo_generator)
- [x] Perform manual integration tests for flows: create event → fetch venues → add RSVPs → generate to-dos → export

## 7. Documentation and Deployment
- [x] Create README.md (step-by-step local setup, how to create API keys (Eventbrite, Google Sheets), how to configure .env, how to run tests, and how to deploy)
- [x] Create docs/design.md (Google Sheets setup, etc.)
- [x] Create scripts/run_local.sh
- [x] Create deploy/README.md (environment variable names and sample commands, choose a free hosting provider and follow their deployment steps in deploy/README.md)
- [x] Include social media caption in README and deployment success message

## 8. Final Validation
- [x] Test scenarios: birthday (small budget, 30 guests), corporate conference (large capacity, AV needs), outdoor meetup (weather contingency to-do)
- [x] Verify acceptance checklist: event input works and validates, venue suggestions return top 5 with rationale, RSVP manager updates status and syncs to Google Sheets, to-do generator produces a 3-tier timeline and is editable, export works (CSV/JSON/PDF), automated email confirmations send successfully
