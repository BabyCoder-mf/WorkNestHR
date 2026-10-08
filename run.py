from datetime import datetime
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import Staff

app = create_app()

with app.app_context():
    db.create_all()

    test_staff = Staff.query.filter_by(employee_id='TEST001').first()
    if not test_staff:
        print("Seeding TEST001...")
        test_staff = Staff(
            employee_id='TEST001',
            name='Jane Doe',
            email='jane.doe@worknest.com',
            age=28,
            sex='Female',
            country='Uganda',
            contract_start=datetime(2025, 1, 1).date(),
            contract_end=datetime(2025, 12, 31).date(),
            position='HR Assistant',
            department='HR',
            location='Kampala',
            pin_hash=generate_password_hash('1234'),
            face_image_url=None,
            is_active=True,
            is_admin=True
        )
        db.session.add(test_staff)
        db.session.commit()
        print("Seeded TEST001. Login: TEST001 / 1234")
    else:
        print("TEST001 already exists, skipping seed.")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
