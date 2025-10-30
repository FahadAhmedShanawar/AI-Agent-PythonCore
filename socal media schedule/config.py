import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API v2
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Meta Graph API (Facebook & Instagram)
META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
META_PAGE_ID = os.getenv('META_PAGE_ID')  # For Facebook page
META_INSTAGRAM_ACCOUNT_ID = os.getenv('META_INSTAGRAM_ACCOUNT_ID')  # For Instagram business account

# App settings
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
