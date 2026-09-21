# reset_database.py
from app import create_app, db
from app.models import Staff, Attendance
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Drop all tables and create new ones with updated schema
    db.drop_all()
    db.create_all()
    print("✅ Database recreated with new schema!")

    # Create test staff with face_image_url
    test_staff = Staff(
        employee_id='TEST001',
        name='John Doe',
        email='john.doe@worknest.com',
        department='IT',
        position='Developer',
        pin_hash=generate_password_hash('1234'),
        face_image_url='https://i.imgur.com/nVFJXWU.jpeg',  # Your Imgur URL
        is_active=True
    )
    db.session.add(test_staff)
    db.session.commit()
    print(f"✅ Test staff created with Imgur URL: {test_staff.face_image_url}")