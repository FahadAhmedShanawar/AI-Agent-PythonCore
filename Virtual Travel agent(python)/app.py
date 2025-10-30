from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv
import yaml
from services import geocoding, flights_service, hotels_service, attractions_service
from utils import cost_estimator, cache_manager
import logging
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Load configuration
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Setup logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize cache
cache = cache_manager.CacheManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    try:
        data = request.get_json()

        # Extract user preferences
        destination = data.get('destination')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        travelers = int(data.get('travelers', 1))
        budget = float(data.get('budget', 1000))
        travel_style = data.get('travel_style', 'balanced')

        # Validate inputs
        if not all([destination, start_date, end_date]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Geocode destination
        coords = geocoding.get_coordinates(destination)
        if not coords:
            return jsonify({'error': 'Destination not found'}), 400

        # Fetch flight data
        flights = flights_service.search_flights(destination, start_date, end_date, travelers)

        # Fetch hotel data
        hotels = hotels_service.search_hotels(coords, start_date, end_date, travelers, budget)

        # Fetch attractions
        attractions = attractions_service.get_attractions(coords, travel_style)

        # Generate itinerary
        itinerary = generate_detailed_itinerary(
            destination, start_date, end_date, travelers, budget, travel_style,
            flights, hotels, attractions
        )

        # Calculate costs
        costs = cost_estimator.calculate_total_cost(itinerary, travelers)

        # Cache the result
        cache_key = f"{destination}_{start_date}_{end_date}_{travelers}_{budget}_{travel_style}"
        cache.set(cache_key, {
            'itinerary': itinerary,
            'costs': costs,
            'timestamp': datetime.now().isoformat()
        })

        return jsonify({
            'itinerary': itinerary,
            'costs': costs,
            'destination': destination
        })

    except Exception as e:
        logging.error(f"Error generating itinerary: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/export/<format_type>')
def export_itinerary(format_type):
    # Implementation for PDF/CSV export
    # This would use reportlab for PDF and pandas for CSV
    pass

def generate_detailed_itinerary(destination, start_date, end_date, travelers, budget, style, flights, hotels, attractions):
    # Basic itinerary generation logic
    # This would be expanded with more sophisticated planning
    itinerary = {
        'destination': destination,
        'duration': f"{start_date} to {end_date}",
        'travelers': travelers,
        'style': style,
        'days': []
    }

    # Generate day-by-day plan (simplified)
    from datetime import datetime, timedelta
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    days = (end - start).days + 1

    for day in range(1, min(days, 8)):  # Max 7 days
        day_plan = {
            'day': day,
            'date': (start + timedelta(days=day-1)).strftime('%Y-%m-%d'),
            'activities': [
                {'time': '09:00', 'activity': 'Breakfast at hotel', 'type': 'meal'},
                {'time': '10:00', 'activity': f'Visit {attractions[day-1]["name"] if day-1 < len(attractions) else "Local attraction"}', 'type': 'attraction'},
                {'time': '13:00', 'activity': 'Lunch at local restaurant', 'type': 'meal'},
                {'time': '15:00', 'activity': 'Free time / Shopping', 'type': 'free'},
                {'time': '19:00', 'activity': 'Dinner and local cuisine experience', 'type': 'meal'}
            ]
        }
        itinerary['days'].append(day_plan)

    return itinerary

if __name__ == '__main__':
    app.run(debug=config['app']['debug'], host='0.0.0.0', port=5000)
