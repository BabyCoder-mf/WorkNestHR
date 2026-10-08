import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'

    _db_url = os.environ.get('DATABASE_URL')
    if _db_url and _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = _db_url or ('sqlite:///' + os.path.join(BASE_DIR, 'worknest_hr.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FACE_API_KEY = os.environ.get('FACE_API_KEY', 'your-facepp-api-key')
    FACE_API_SECRET = os.environ.get('FACE_API_SECRET', 'your-facepp-api-secret')
    FACE_API_REGION = os.getenv('FACE_API_REGION', 'us')
    IMGUR_CLIENT_ID = os.environ.get('IMGUR_CLIENT_ID', 'your-imgur-client-id')
