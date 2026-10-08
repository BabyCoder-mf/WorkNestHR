import os
from dotenv import load_dotenv

load_dotenv()

# This calculates the exact absolute directory path of your project folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:  # Exactly "Config" matching your original file
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    
    # FIXED ABSOLUTE PATH: This forces Render to stay locked onto your database file
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'worknest_hr.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Face++ API Configuration
    FACE_API_KEY = os.environ.get('FACE_API_KEY', 'your-facepp-api-key')
    FACE_API_SECRET = os.environ.get('FACE_API_SECRET', 'your-facepp-api-secret')
    FACE_API_REGION = os.getenv('FACE_API_REGION', 'us')  

    # Imgur Configuration - PRESERVED NATIVELY
    IMGUR_CLIENT_ID = os.environ.get('IMGUR_CLIENT_ID', 'your-imgur-client-id')
