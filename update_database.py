# update_database.py
from app import create_app, db
from app.models import Staff

app = create_app()

with app.app_context():
    # This will add any missing columns to existing tables
    db.create_all()
    print("✅ Database updated with new columns!")

    # Set your Imgur URL for the test staff
    test_staff = Staff.query.filter_by(employee_id='TEST001').first()
    if test_staff:
        test_staff.face_image_url = 'https://i.imgur.com/nVFJXWU.jpeg'
        db.session.commit()
        print(f"✅ Set Imgur URL for {test_staff.name}: {test_staff.face_image_url}")
    else:
        print("❌ Test staff not found. Please create test data first.")