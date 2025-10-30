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
 



--------------------------------------------------------------
## Don't forget
- This is necessary to create a virtual environment.
- Make sure to install the packages to run the relevant agent.

(venv) folder typically contains:
# Virtual Environment Setup Guide

## Prerequisites
- Python 3.x installed on your system
- pip package manager

## Setting Up Virtual Environment

### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv

# Unix/Linux/MacOS
python3 -m venv venv
```

### 2. Activate Virtual Environment
```bash
# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Unix/Linux/MacOS
source venv/bin/activate
```

### 3. Verify Activation
- Your prompt should now show `(venv)` at the beginning
- Verify Python location:
```bash
which python  # Unix/Linux/MacOS
where python  # Windows
```

### 4. Install Required Packages
```bash
pip install -r requirements.txt
```

### 5. Deactivating Virtual Environment
When you're done working:
```bash
deactivate
```
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


