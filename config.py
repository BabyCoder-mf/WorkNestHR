import os
from dotenv import load_dotenv

load_dotenv()

class Config:  # Make sure this is exactly "Config" (capital C)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///worknest_hr.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Face++ API Configuration
    FACE_API_KEY = os.environ.get('FACE_API_KEY', 'your-facepp-api-key')
    FACE_API_SECRET = os.environ.get('FACE_API_SECRET', 'your-facepp-api-secret')

    # Imgur Configuration
    IMGUR_CLIENT_ID = os.environ.get('IMGUR_CLIENT_ID', 'your-imgur-client-id')