"""Database models for WorkNest HR app"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Staff(db.Model, UserMixin):
    """Staff member model"""

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    country = db.Column(db.String(100))
    contract_start = db.Column(db.Date)
    contract_end = db.Column(db.Date)
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    location = db.Column(db.String(100))
    pin_hash = db.Column(db.String(255))
    face_image_url = db.Column(db.String(500))  # This is the profile photo!
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attendance_records = db.relationship('Attendance', backref='staff', lazy=True)


class Attendance(db.Model):
    """Attendance record model"""

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    check_in_time = db.Column(db.DateTime, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime)
    authentication_method = db.Column(db.String(20))  # 'face' or 'pin'
    location_country = db.Column(db.String(100))
    location_city = db.Column(db.String(100))
    location_ip = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return Staff.query.get(int(user_id))