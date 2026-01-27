# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
# ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Database Configuration
DB_TYPE = 'sqlite'  # or 'mongodb'
SQLITE_DB_PATH = 'data/cyber_intelligence.db'
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')

# Scraping Configuration
REQUEST_DELAY = 2  # seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30

# Data Paths
RAW_DATA_DIR = 'data/raw'
PROCESSED_DATA_DIR = 'data/processed'
