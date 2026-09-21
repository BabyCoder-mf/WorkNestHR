# check_schema.py
from app import create_app, db
from app.models import Staff, Attendance

app = create_app()

with app.app_context():
    print("🔍 DATABASE SCHEMA ANALYSIS")
    print("=" * 50)

    # Staff Table Structure
    print("\n📋 STAFF TABLE STRUCTURE:")
    staff_columns = [(column.name, str(column.type)) for column in Staff.__table__.columns]
    for col_name, col_type in staff_columns:
        print(f"   {col_name}: {col_type}")

    # Attendance Table Structure
    print("\n📋 ATTENDANCE TABLE STRUCTURE:")
    attendance_columns = [(column.name, str(column.type)) for column in Attendance.__table__.columns]
    for col_name, col_type in attendance_columns:
        print(f"   {col_name}: {col_type}")

    # Sample Data
    print("\n📊 SAMPLE DATA:")

    # Staff data
    staff = Staff.query.first()
    if staff:
        print(f"\n👤 STAFF RECORD:")
        print(f"   ID: {staff.id}")
        print(f"   Employee ID: {staff.employee_id}")
        print(f"   Name: {staff.name}")
        print(f"   Email: {staff.email}")
        print(f"   Department: {staff.department}")
        print(f"   Imgur URL: {staff.face_image_url}")
        print(f"   Active: {staff.is_active}")
        print(f"   Created: {staff.created_at}")

    # Attendance data
    attendance = Attendance.query.first()
    if attendance:
        print(f"\n📅 ATTENDANCE RECORD:")
        print(f"   ID: {attendance.id}")
        print(f"   Staff ID: {attendance.staff_id}")
        print(f"   Check-in: {attendance.check_in_time}")
        print(f"   Method: {attendance.authentication_method}")
        print(f"   Country: {attendance.location_country}")
        print(f"   City: {attendance.location_city}")
        print(f"   IP: {attendance.location_ip}")
        print(f"   Created: {attendance.created_at}")

    # Count records
    staff_count = Staff.query.count()
    attendance_count = Attendance.query.count()
    print(f"\n📈 RECORD COUNTS:")
    print(f"   Staff: {staff_count}")
    print(f"   Attendance: {attendance_count}")