# update_attendance_table.py
from app import create_app, db
from app.models import Staff, Attendance
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Drop and recreate all tables to include new columns
    print("🔄 Updating database schema...")
    db.drop_all()
    db.create_all()
    print("✅ Database schema updated with location columns!")

    # Create test staff with face_image_url
    test_staff = Staff(
        employee_id='TEST001',
        name='John Doe',
        email='john.doe@worknest.com',
        department='IT',
        position='Developer',
        pin_hash=generate_password_hash('1234'),
        face_image_url='https://i.imgur.com/nVFJXWU.jpeg',
        is_active=True
    )
    db.session.add(test_staff)
    db.session.commit()
    print(f"✅ Test staff created with Imgur URL: {test_staff.face_image_url}")

    # Verify the attendance table has location columns
    attendance_columns = [column.name for column in Attendance.__table__.columns]
    print(f"📊 Attendance table columns: {attendance_columns}")