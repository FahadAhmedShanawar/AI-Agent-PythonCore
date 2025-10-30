# Virtual Travel Agent

An AI-powered travel planning application that helps users create personalized itineraries with flights, accommodations, attractions, and cost estimates.

## Features

- **Preference Input**: Collect destination, dates, travelers, budget, and travel style
- **Flight Search**: Integration with Skyscanner API for flight options
- **Accommodation Finder**: Hotel search via Skyscanner or open data APIs
- **Attraction Suggestions**: POI recommendations using OpenTripMap API
- **Cost Estimation**: Transparent pricing with per-person totals
- **Dynamic Itineraries**: Day-by-day plans with times, distances, and commute estimates
- **Export Options**: PDF and CSV itinerary summaries
- **Caching & Logging**: Efficient API usage and error handling

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your API keys
6. Run the app: `python app.py`
7. 


--------------------------------------------------------------
## Don't forget
- This is necessary to create a virtual environment.
- Make sure to install the packages to run the relevant agent.
---------------------------------------------------------------



## API Keys Required

- Skyscanner API (for flights and hotels)
- OpenTripMap API (for attractions)
- Unsplash API (for destination images)

## Usage

1. Open the web interface
2. Enter your travel preferences
3. Generate your personalized itinerary
4. Export or share your plan

## Project Structure

- `app.py`: Main Flask application
- `config/`: Configuration files
- `services/`: API integration modules
- `utils/`: Helper functions and utilities
- `templates/`: HTML templates
- `static/`: CSS and images
- `tests/`: Test files
- `docs/`: Documentation

## Contributing

Please read the usage guide in `docs/usage_guide.md` for detailed setup and development instructions.

