# Virtual Travel Agent - Usage Guide

## Overview

The Virtual Travel Agent is an AI-powered web application that helps users plan personalized travel itineraries. It integrates with multiple APIs to provide comprehensive travel planning including flights, accommodations, attractions, and cost estimates.

## Features

- **User-Friendly Interface**: Simple web form for inputting travel preferences
- **API Integration**: Connects to Skyscanner, OpenTripMap, Nominatim, and Unsplash APIs
- **Dynamic Itineraries**: Generates day-by-day plans based on travel style
- **Cost Estimation**: Transparent pricing with breakdowns
- **Export Options**: PDF and CSV export functionality
- **Caching System**: Efficient API usage with local caching

## Prerequisites

- Python 3.8+
- pip package manager
- API keys for external services

## Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd virtual-travel-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Add your API keys:
     ```
     SKYSCANNER_API_KEY=your_skyscanner_key
     OPENTRIPMAP_API_KEY=your_opentripmap_key
     UNSPLASH_ACCESS_KEY=your_unsplash_key
     ```

## Configuration

The application uses `config/config.yaml` for configuration. Key settings include:

- Currency and timezone defaults
- Cache expiry times
- API endpoints and limits
- Travel style categories

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   - Navigate to `http://localhost:5000`
   - Fill out the travel planning form
   - Generate your itinerary

## API Keys Setup

### Skyscanner API
- Sign up at [RapidAPI Skyscanner](https://rapidapi.com/skyscanner/api/skyscanner-flight-search)
- Get your API key
- Add to `.env` as `SKYSCANNER_API_KEY`

### OpenTripMap API
- Get API key from [OpenTripMap](https://opentripmap.io/)
- Add to `.env` as `OPENTRIPMAP_API_KEY`

### Unsplash API
- Create app at [Unsplash Developers](https://unsplash.com/developers)
- Get access key
- Add to `.env` as `UNSPLASH_ACCESS_KEY`

## Usage Workflow

1. **Input Preferences**
   - Enter destination city/country
   - Select travel dates
   - Specify number of travelers
   - Set budget per person
   - Choose travel style (relaxed, adventure, family, luxury)

2. **Generate Itinerary**
   - Click "Generate My Itinerary"
   - Wait for processing (may take a few seconds)
   - View detailed day-by-day plan

3. **Review Results**
   - Check cost breakdown
   - Review daily activities
   - View travel tips

4. **Export/Share**
   - Download PDF or CSV
   - Share on social media

## Travel Styles

- **Relaxed**: Museums, parks, beaches, historic sites
- **Adventure**: Mountains, hiking, sports, natural attractions
- **Family**: Museums, zoos, aquariums, amusement parks
- **Luxury**: High-end museums, historic sites, galleries, theatres

## Cost Estimation

Costs are estimated based on:
- Flight prices (economy class)
- Hotel rates (3-5 star depending on budget)
- Activity fees and entrance tickets
- Miscellaneous expenses (10% buffer)

## Caching

The application caches API responses to:
- Reduce API calls and costs
- Improve response times
- Handle temporary API outages

Cache settings in `config/config.yaml`:
- Default expiry: 24 hours
- Storage: SQLite database in `cache/` directory

## Testing

Run the test suite:
```bash
python -m unittest tests/test_itinerary.py
```

Tests cover:
- API integrations
- Cost calculations
- Cache functionality
- Data validation

## Troubleshooting

### Common Issues

1. **"Destination not found"**
   - Check spelling of destination
   - Try using city, country format

2. **API errors**
   - Verify API keys in `.env`
   - Check API service status
   - Review rate limits

3. **No results**
   - Try different dates
   - Adjust budget or travel style
   - Check internet connection

### Logs

Check `logs/app.log` for detailed error information.

## Development

### Project Structure
```
virtual-travel-agent/
├── app.py                 # Main Flask application
├── config/
│   └── config.yaml       # Configuration settings
├── services/             # API integration modules
├── utils/               # Helper utilities
├── templates/           # HTML templates
├── static/              # CSS and images
├── tests/               # Test files
├── docs/                # Documentation
└── cache/               # Cached data
```

### Adding New Features

1. Create new service in `services/`
2. Add utility functions in `utils/`
3. Update routes in `app.py`
4. Add tests in `tests/`
5. Update documentation

## Checklist Status

- ✅ Preference input system
- ✅ Geocoding working
- ✅ Flight and hotel search integrated
- ✅ Attractions displayed via OpenTripMap
- ✅ Itinerary generator outputs structured plans
- ✅ PDF/CSV export functional
- ✅ Caching & logging implemented
- ✅ Tests passed
- ✅ Documentation updated

## Support

For issues or questions:
1. Check this usage guide
2. Review error logs
3. Test with different inputs
4. Verify API key configuration

## License

This project is open source. Please check the license file for details.
