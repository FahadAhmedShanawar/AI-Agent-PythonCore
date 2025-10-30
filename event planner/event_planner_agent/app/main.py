from flask import Flask
from dotenv import load_dotenv
import os
import logging
from routes import register_routes

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '..', 'logs', 'app.log'),
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

    # Register routes
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
