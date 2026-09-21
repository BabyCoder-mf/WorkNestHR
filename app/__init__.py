from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import sqlite3

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Direct configuration with YOUR actual API keys
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-12345')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///worknest_hr.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # YOUR ACTUAL FACE++ API KEYS
    app.config['FACE_API_KEY'] = os.environ.get('FACE_API_KEY', 'pnchrZkmOYajxRRWUvWRaiRfMgVKmmzA')
    app.config['FACE_API_SECRET'] = os.environ.get('FACE_API_SECRET', '41LgzmyY-s7rEEF8HTNhV9-lXpJav1ba')

    # Imgur (we'll use this later for storing face photos)
    app.config['IMGUR_CLIENT_ID'] = os.environ.get('IMGUR_CLIENT_ID', 'your_imgur_client_id')

    print("✅ App configured with REAL Face++ API keys!")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # FORCE CREATE admin_faces table BEFORE app context
    print("\n🔄 Ensuring admin_faces table exists...")
    try:
        conn = sqlite3.connect('worknest_hr.db')
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_username TEXT NOT NULL UNIQUE,
                face_image TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

        # Verify
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin_faces'")
        if cursor.fetchone():
            print("✅ admin_faces table verified")
        else:
            print("❌ admin_faces table creation failed")

        # Show all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"📊 All tables: {tables}")

        conn.close()
    except Exception as e:
        print(f"❌ Error creating admin_faces table: {e}")

    # Create other tables in app context
    with app.app_context():
        db.create_all()
        print("✅ All SQLAlchemy tables created")

    from app.routes import main
    app.register_blueprint(main)

    return app