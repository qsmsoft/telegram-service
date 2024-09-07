import os

from dotenv import load_dotenv

load_dotenv()

# database configuration
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# telegram configuration
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

# jwt authentication configuration
secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
access_token_expire_minutes = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')