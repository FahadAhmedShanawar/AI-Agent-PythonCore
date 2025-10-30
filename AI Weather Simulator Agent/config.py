import os
from dotenv import load_dotenv

load_dotenv()

# API Keys - Add your keys to a .env file
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
METEOSTAT_API_KEY = os.getenv('METEOSTAT_API_KEY')  # If needed
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# API URLs
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
METEOSTAT_BASE_URL = "https://api.meteostat.net/v2"

# App Configuration
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
