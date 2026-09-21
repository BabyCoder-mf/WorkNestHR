"""Routes for WorkNest HR app - COMPLETE WORKING VERSION"""
from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, request, current_app, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Staff, Attendance

main = Blueprint('main', __name__)

# Temporary admin credentials (for demo purposes)
ADMIN_CREDENTIALS = {
    "admin": {
        "pin": "1234",
        "name": "System Administrator",
        "email": "admin@worknest.com"
    },
    "hr": {
        "pin": "5678",
        "name": "HR Manager",
        "email": "hr@worknest.com"
    }
}

@main.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@main.route('/register-face')
def register_face_page():
    """Page for registering faces (hidden admin page)"""
    return render_template('register_face.html')

@main.route('/profile')
def profile():
    """Employee profile page with full details"""
    # For now, just get the first staff member
    staff = Staff.query.filter_by(employee_id='TEST001').first()
    if not staff:
        return "Staff not found", 404

    # Debug: print staff data to console to verify all fields are populated
    print(f"=== STAFF DATA ===")
    print(f"Name: {staff.name}")
    print(f"Age: {staff.age}")
    print(f"Sex: {staff.sex}")
    print(f"Country: {staff.country}")
    print(f"Position: {staff.position}")
    print(f"Location: {staff.location}")
    print(f"Department: {staff.department}")
    print(f"Contract Start: {staff.contract_start}")
    print(f"Contract End: {staff.contract_end}")
    print(f"==================")

    return render_template('profile.html', staff=staff)

@main.route('/admin/login')
def admin_login_page():
    """Admin login page"""
    return render_template('admin_login.html')

@main.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page with statistics"""
    try:
        # Get statistics
        total_employees = Staff.query.filter_by(is_active=True).count()
        total_attendance = Attendance.query.count()

        # Today's attendance count
        from datetime import datetime, date
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = datetime.combine(date.today(), datetime.max.time())

        today_attendance = Attendance.query.filter(
            Attendance.check_in_time >= today_start,
            Attendance.check_in_time <= today_end
        ).count()

        # Mock data for demo
        pending_leaves = 3  # This would come from a Leave model

        # ============================================
        # REAL RECENT ACTIVITY - FROM DATABASE
        # ============================================
        # Get recent check-ins (last 5)
        recent_checkins = Attendance.query\
            .join(Staff, Attendance.staff_id == Staff.id)\
            .order_by(Attendance.check_in_time.desc())\
            .limit(5)\
            .all()

        recent_activity = []

        for checkin in recent_checkins:
            # Calculate time difference
            from datetime import datetime
            time_diff = datetime.utcnow() - checkin.check_in_time
            hours_ago = int(time_diff.total_seconds() / 3600)

            if hours_ago < 1:
                time_text = "just now"
            elif hours_ago == 1:
                time_text = "1 hour ago"
            elif hours_ago < 24:
                time_text = f"{hours_ago} hours ago"
            else:
                days_ago = hours_ago // 24
                time_text = f"{days_ago} day{'s' if days_ago > 1 else ''} ago"

            # Determine icon and color based on authentication method
            if checkin.authentication_method == 'face':
                icon = "person-check"
                color = "success"
                method_text = "checked in with face recognition"
            else:
                icon = "key"
                color = "primary"
                method_text = "checked in with PIN"

            recent_activity.append({
                "icon": icon,
                "color": color,
                "message": f"{checkin.staff.name} {method_text}",
                "time": time_text
            })

        # If no recent activity, show placeholder
        if not recent_activity:
            recent_activity = [
                {"icon": "info-circle", "color": "info", "message": "No recent activity yet", "time": "just now"}
            ]

        # Get all staff for the admin face upload dropdown
        all_staff = Staff.query.filter_by(is_active=True).all()

        # Get admin staff (TEST001)
        admin_staff = Staff.query.filter_by(employee_id='TEST001').first()

        # Admin data with actual profile image
        admin_data = {
            "name": admin_staff.name if admin_staff else "System Administrator",
            "email": admin_staff.email if admin_staff else "admin@worknest.com",
            "username": "admin",
            "profile_image_url": admin_staff.face_image_url if admin_staff else None
        }

        return render_template('admin_dashboard.html',
                            stats={
                                'total_employees': total_employees,
                                'today_attendance': today_attendance,
                                'pending_leaves': pending_leaves,
                                'total_attendance': total_attendance
                            },
                            recent_activity=recent_activity,
                            admin_data=admin_data,
                            all_staff=all_staff)

    except Exception as e:
        print(f"Error loading dashboard: {str(e)}")
        return f"Error loading dashboard: {str(e)}", 500


    """Admin dashboard page with statistics"""
    try:
        # Get statistics
        total_employees = Staff.query.filter_by(is_active=True).count()
        total_attendance = Attendance.query.count()

        # Today's attendance count
        from datetime import datetime, date
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = datetime.combine(date.today(), datetime.max.time())

        today_attendance = Attendance.query.filter(
            Attendance.check_in_time >= today_start,
            Attendance.check_in_time <= today_end
        ).count()

        # Mock data for demo
        pending_leaves = 3  # This would come from a Leave model

        # Recent activity (mock data for demo)
        recent_activity = [
            {"icon": "person-check", "color": "success", "message": "Jane Doe checked in", "time": "2 hours ago"},
            {"icon": "clock", "color": "warning", "message": "Leave request submitted", "time": "4 hours ago"},
            {"icon": "person-plus", "color": "primary", "message": "New employee registered", "time": "1 day ago"},
            {"icon": "calendar-check", "color": "info", "message": "Monthly report generated", "time": "2 days ago"}
        ]

        # Get all staff for the admin face upload dropdown
        all_staff = Staff.query.filter_by(is_active=True).all()

        # Get admin staff (TEST001)
        admin_staff = Staff.query.filter_by(employee_id='TEST001').first()

        # Admin data with actual profile image
        admin_data = {
            "name": admin_staff.name if admin_staff else "System Administrator",
            "email": admin_staff.email if admin_staff else "admin@worknest.com",
            "username": "admin",
            "profile_image_url": admin_staff.face_image_url if admin_staff else None
        }

        return render_template('admin_dashboard.html',
                            stats={
                                'total_employees': total_employees,
                                'today_attendance': today_attendance,
                                'pending_leaves': pending_leaves,
                                'total_attendance': total_attendance
                            },
                            recent_activity=recent_activity,
                            admin_data=admin_data,
                            all_staff=all_staff)

    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

@main.route('/admin/employees')
def manage_employees():
    """Employee management page"""
    try:
        # Get all employees
        employees = Staff.query.all()
        return render_template('manage_employees.html', employees=employees)
    except Exception as e:
        return f"Error loading employees: {str(e)}", 500

@main.route('/api/test-db')
def test_db():
    """Test database connection"""
    try:
        staff_count = Staff.query.count()
        return jsonify({
            'status': 'success',
            'message': 'Database is working!',
            'staff_count': staff_count
        })
    except Exception as e:  # pylint: disable=broad-except
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main.route('/api/create-test-data')
def create_test_data():
    """Create test staff and attendance data"""
    try:
        # Check if test staff already exists
        test_staff = Staff.query.filter_by(employee_id='TEST001').first()
        if not test_staff:
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
                face_image_url='https://via.placeholder.com/150',
                is_active=True,
                is_admin=True  # Make this staff an admin as well
            )
            db.session.add(test_staff)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Test staff created with all details!',
                'staff': {
                    'id': test_staff.id,
                    'name': test_staff.name,
                    'employee_id': test_staff.employee_id,
                    'age': test_staff.age,
                    'sex': test_staff.sex,
                    'country': test_staff.country,
                    'position': test_staff.position,
                    'location': test_staff.location,
                    'department': test_staff.department,
                    'is_admin': test_staff.is_admin
                }
            })
        else:
            # Update existing staff with all fields
            test_staff.name = 'Jane Doe'
            test_staff.email = 'jane.doe@worknest.com'
            test_staff.age = 28
            test_staff.sex = 'Female'
            test_staff.country = 'Uganda'
            test_staff.contract_start = datetime(2025, 1, 1).date()
            test_staff.contract_end = datetime(2025, 12, 31).date()
            test_staff.position = 'HR Assistant'
            test_staff.department = 'HR'
            test_staff.location = 'Kampala'
            test_staff.pin_hash = generate_password_hash('1234')
            test_staff.is_admin = True  # Make admin
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Test staff updated with all details!',
                'staff': {
                    'id': test_staff.id,
                    'name': test_staff.name,
                    'employee_id': test_staff.employee_id,
                    'age': test_staff.age,
                    'sex': test_staff.sex,
                    'country': test_staff.country,
                    'position': test_staff.position,
                    'location': test_staff.location,
                    'department': test_staff.department,
                    'is_admin': test_staff.is_admin
                }
            })

    except Exception as e:  # pylint: disable=broad-except
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main.route('/api/admin-login', methods=['POST'])
def admin_login_api():
    """Admin login with username and PIN"""
    try:
        data = request.get_json()
        username = data.get('username')
        pin = data.get('pin')

        if not username or not pin:
            return jsonify({'success': False, 'message': 'Username and PIN required'})

        # Check against temporary credentials
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username]['pin'] == pin:
            # Set session
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['admin_name'] = ADMIN_CREDENTIALS[username]['name']

            return jsonify({
                'success': True,
                'message': f'Welcome {ADMIN_CREDENTIALS[username]["name"]}!',
                'admin': {
                    'username': username,
                    'name': ADMIN_CREDENTIALS[username]['name'],
                    'email': ADMIN_CREDENTIALS[username]['email']
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid username or PIN'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500

# ============================================================================
# EMPLOYEE MANAGEMENT API ROUTES
# ============================================================================

@main.route('/api/employees', methods=['GET'])
def get_employees_api():
    """Get all employees (API endpoint)"""
    try:
        employees = Staff.query.all()
        employees_list = []
        for emp in employees:
            employees_list.append({
                'id': emp.id,
                'employee_id': emp.employee_id,
                'name': emp.name,
                'email': emp.email,
                'position': emp.position,
                'department': emp.department,
                'location': emp.location,
                'is_active': emp.is_active,
                'face_image_url': emp.face_image_url
            })
        return jsonify(employees_list)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get specific employee details"""
    try:
        employee = Staff.query.get(employee_id)
        if not employee:
            return jsonify({'success': False, 'message': 'Employee not found'}), 404

        employee_data = {
            'id': employee.id,
            'employee_id': employee.employee_id,
            'name': employee.name,
            'email': employee.email,
            'age': employee.age,
            'sex': employee.sex,
            'country': employee.country,
            'contract_start': employee.contract_start.isoformat() if employee.contract_start else None,
            'contract_end': employee.contract_end.isoformat() if employee.contract_end else None,
            'position': employee.position,
            'department': employee.department,
            'location': employee.location,
            'is_active': employee.is_active,
            'is_admin': employee.is_admin,
            'face_image_url': employee.face_image_url,
            'created_at': employee.created_at.isoformat() if employee.created_at else None
        }

        return jsonify(employee_data)

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/api/employees', methods=['POST'])
def create_employee():
    """Create new employee"""
    try:
        data = request.get_json()

        # Check if employee ID already exists
        existing_employee = Staff.query.filter_by(employee_id=data.get('employee_id')).first()
        if existing_employee:
            return jsonify({'success': False, 'message': 'Employee ID already exists'})

        # Create new employee
        new_employee = Staff(
            employee_id=data.get('employee_id'),
            name=data.get('name'),
            email=data.get('email'),
            position=data.get('position'),
            department=data.get('department'),
            location=data.get('location'),
            pin_hash=generate_password_hash(data.get('pin', '1234')),  # Default PIN
            is_active=data.get('is_active', True),
            face_image_url='https://via.placeholder.com/150'  # Default placeholder
        )

        db.session.add(new_employee)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Employee created successfully',
            'employee_id': new_employee.employee_id
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update employee details"""
    try:
        data = request.get_json()
        employee = Staff.query.get(employee_id)

        if not employee:
            return jsonify({'success': False, 'message': 'Employee not found'})

        # Update all fields
        employee.name = data.get('name', employee.name)
        employee.email = data.get('email', employee.email)
        employee.age = data.get('age', employee.age)
        employee.sex = data.get('sex', employee.sex)
        employee.country = data.get('country', employee.country)
        employee.position = data.get('position', employee.position)
        employee.department = data.get('department', employee.department)
        employee.location = data.get('location', employee.location)
        employee.is_active = data.get('is_active', employee.is_active)
        employee.is_admin = data.get('is_admin', employee.is_admin)

        # Handle date fields
        if data.get('contract_start'):
            employee.contract_start = datetime.strptime(data.get('contract_start'), '%Y-%m-%d').date()
        if data.get('contract_end'):
            employee.contract_end = datetime.strptime(data.get('contract_end'), '%Y-%m-%d').date()

        # Update PIN if provided
        if data.get('pin'):
            employee.pin_hash = generate_password_hash(data.get('pin'))

        db.session.commit()

        return jsonify({'success': True, 'message': 'Employee updated successfully'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@main.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete employee (soft delete)"""
    try:
        employee = Staff.query.get(employee_id)

        if not employee:
            return jsonify({'success': False, 'message': 'Employee not found'})

        # Soft delete - set as inactive
        employee.is_active = False
        db.session.commit()

        return jsonify({'success': True, 'message': 'Employee deleted successfully'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================================================
# FACE RECOGNITION & AUTHENTICATION ROUTES
# ============================================================================

@main.route('/api/pin-login', methods=['POST'])
def pin_login():
    """Employee PIN login"""
    try:
        data = request.get_json()
        employee_id = data.get('employee_id')
        pin = data.get('pin')

        if not employee_id or not pin:
            return jsonify({'success': False, 'message': 'Employee ID and PIN required'})

        # Find active employee
        employee = Staff.query.filter_by(employee_id=employee_id, is_active=True).first()

        if employee and check_password_hash(employee.pin_hash, pin):
            # Create attendance record
            from app.services.location_service import LocationService
            location_service = LocationService()
            location_info = location_service.get_location_info()

            attendance = Attendance(
                staff_id=employee.id,
                authentication_method='pin',
                check_in_time=datetime.utcnow(),
                location_country=location_info['country'],
                location_city=location_info['city'],
                location_ip=location_info['ip']
            )
            db.session.add(attendance)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': f'Welcome {employee.name}!',
                'staff': {
                    'id': employee.id,
                    'name': employee.name,
                    'employee_id': employee.employee_id,
                    'department': employee.department
                },
                'location': {
                    'country': location_info['country'],
                    'city': location_info['city'],
                    'time': datetime.utcnow().strftime('%H:%M')
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid Employee ID or PIN'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'PIN login error: {str(e)}'
        }), 500

@main.route('/api/test-facepp')
def test_facepp():
    """Test Face++ API connection"""
    try:
        from app.services.facepp_service import FacePlusPlusService
        face_service = FacePlusPlusService()

        # Test by creating faceset
        success = face_service.create_faceset()

        if success:
            return jsonify({
                'success': True,
                'message': 'Face++ API is working correctly!',
                'api_key': f"{current_app.config['FACE_API_KEY'][:8]}..."  # Show first 8 chars
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Face++ API test failed. Check your credentials.'
            })

    except Exception as e:  # pylint: disable=broad-except
        return jsonify({
            'success': False,
            'message': f'Face++ test error: {str(e)}'
        }), 500

@main.route('/api/get-staff')
def get_staff():
    """Get all staff members for registration"""
    try:
        staff = Staff.query.filter_by(is_active=True).all()
        staff_list = []
        for s in staff:
            staff_list.append({
                'id': s.id,
                'name': s.name,
                'employee_id': s.employee_id,
                'department': s.department,
                'has_face': s.face_image_url is not None
            })
        return jsonify(staff_list)
    except Exception as e:  # pylint: disable=broad-except
        return jsonify([])

@main.route('/api/face-login', methods=['POST'])
def face_login():
    """Compare live face photo with stored base64 face images"""
    try:
        data = request.get_json()
        live_image_data = data.get('image_data')

        print("=== FACE LOGIN DEBUG ===")
        print(f"Live image data received: {len(live_image_data) if live_image_data else 0} chars")

        if not live_image_data:
            return jsonify({
                'success': False,
                'message': 'No image data provided'
            })

        from app.services.facepp_service import FacePlusPlusService
        from app.services.location_service import LocationService

        face_service = FacePlusPlusService()
        location_service = LocationService()

        # Get all active staff with face images
        staff_with_faces = Staff.query.filter_by(is_active=True).filter(Staff.face_image_url.isnot(None)).all()

        print(f"Found {len(staff_with_faces)} staff with face images")

        if not staff_with_faces:
            return jsonify({
                'success': False,
                'message': 'No staff faces registered in system'
            })

        best_match = None
        highest_confidence = 0

        # Compare with each staff member's base64 photo
        for staff in staff_with_faces:
            print(f"Comparing with {staff.name}")

            # Extract base64 data from data URL
            if staff.face_image_url and staff.face_image_url.startswith('data:image'):
                try:
                    stored_base64 = staff.face_image_url.split(',')[1]

                    confidence, success = face_service.compare_faces(
                        live_image_data,        # Base64 from camera
                        stored_base64,          # Base64 from database
                        image1_is_url=False,    # Both are base64, not URLs
                        image2_is_url=False
                    )

                    print(f"Comparison with {staff.name}: success={success}, confidence={confidence}")

                    if success and confidence > highest_confidence:
                        highest_confidence = confidence
                        best_match = staff
                except Exception as e:
                    print(f"Error comparing with {staff.name}: {e}")
                    continue
            else:
                print(f"Skipping {staff.name} - no valid base64 face image")

        print(f"Best match: {best_match.name if best_match else 'None'} with {highest_confidence}% confidence")

        # Check if we have a good match
        if best_match and highest_confidence >= 80:
            # Check if already checked in today
            from datetime import datetime, date
            today_start = datetime.combine(date.today(), datetime.min.time())
            today_end = datetime.combine(date.today(), datetime.max.time())

            existing_attendance = Attendance.query.filter(
                Attendance.staff_id == best_match.id,
                Attendance.check_in_time >= today_start,
                Attendance.check_in_time <= today_end
            ).first()

            # Get location information
            location_info = location_service.get_location_info()

            if existing_attendance:
                # Already checked in today - auto redirect to profile
                return jsonify({
                    'success': True,
                    'message': 'Welcome back!',
                    'staff': {
                        'id': best_match.id,
                        'name': best_match.name,
                        'employee_id': best_match.employee_id,
                        'department': best_match.department
                    },
                    'confidence': highest_confidence,
                    'location': {
                        'country': location_info['country'],
                        'city': location_info['city'],
                        'time': datetime.utcnow().strftime('%H:%M')
                    },
                    'already_checked_in': True
                })

            # Create attendance record with location (first time today)
            attendance = Attendance(
                staff_id=best_match.id,
                authentication_method='face',
                check_in_time=datetime.utcnow(),
                location_country=location_info['country'],
                location_city=location_info['city'],
                location_ip=location_info['ip']
            )
            db.session.add(attendance)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': f'Welcome {best_match.name}!',
                'staff': {
                    'id': best_match.id,
                    'name': best_match.name,
                    'employee_id': best_match.employee_id,
                    'department': best_match.department
                },
                'confidence': highest_confidence,
                'location': {
                    'country': location_info['country'],
                    'city': location_info['city'],
                    'time': datetime.utcnow().strftime('%H:%M')
                },
                'already_checked_in': False
            })
        elif best_match and highest_confidence >= 60:
            return jsonify({
                'success': False,
                'message': f'Low confidence match ({highest_confidence}%). Please try again.',
                'confidence': highest_confidence
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No matching face found. Please try PIN login.'
            })

    except Exception as e:
        print(f"Face login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Face recognition error: {str(e)}'
        }), 500

@main.route('/api/init-faceset', methods=['POST'])
def init_faceset():
    """Initialize Face++ faceset"""
    try:
        from app.services.facepp_service import FacePlusPlusService
        face_service = FacePlusPlusService()

        if face_service.create_faceset():
            return jsonify({
                'success': True,
                'message': 'Face++ faceset initialized successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to initialize faceset'
            })

    except Exception as e:  # pylint: disable=broad-except
        return jsonify({
            'success': False,
            'message': f'Faceset initialization error: {str(e)}'
        }), 500

@main.route('/api/upload-face-photo', methods=['POST'])
def upload_face_photo():
    """Upload face photo - store as base64 data URL in database"""
    try:
        data = request.get_json()
        staff_id = data.get('staff_id')
        image_data = data.get('image_data')

        if not staff_id or not image_data:
            return jsonify({
                'success': False,
                'message': 'Staff ID and image data required'
            })

        staff = Staff.query.get(staff_id)
        if not staff:
            return jsonify({'success': False, 'message': 'Staff not found'})

        # Create data URL for direct display
        image_url = f"data:image/jpeg;base64,{image_data}"

        # Update the face image in database
        staff.face_image_url = image_url
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Face photo uploaded successfully!',
            'image_url': image_url
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error uploading photo: {str(e)}'
        }), 500

@main.route('/api/admin-upload-face', methods=['POST'])
def admin_upload_face():
    """Admin route to upload face photos for any employee"""
    try:
        data = request.get_json()
        staff_id = data.get('staff_id')
        image_data = data.get('image_data')

        if not staff_id or not image_data:
            return jsonify({
                'success': False,
                'message': 'Staff ID and image data required'
            })

        staff = Staff.query.get(staff_id)
        if not staff:
            return jsonify({'success': False, 'message': 'Staff not found'})

        # Create data URL for direct display
        image_url = f"data:image/jpeg;base64,{image_data}"

        # Update the face image in database
        staff.face_image_url = image_url
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Face photo uploaded successfully for {staff.name}!',
            'image_url': image_url,
            'staff': {
                'id': staff.id,
                'name': staff.name,
                'employee_id': staff.employee_id
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error uploading photo: {str(e)}'
        }), 500

@main.route('/api/get-current-location')
def get_current_location():
    """Get current location for profile page"""
    try:
        from app.services.location_service import LocationService
        location_service = LocationService()
        location_info = location_service.get_location_info()

        return jsonify({
            'success': True,
            'country': location_info['country'],
            'city': location_info['city'],
            'ip': location_info['ip']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Location error: {str(e)}'
        }), 500

@main.route('/api/debug-employee/<employee_id>')
def debug_employee(employee_id):
    """Debug endpoint to check employee data"""
    try:
        staff = Staff.query.filter_by(employee_id=employee_id).first()
        if not staff:
            return jsonify({'success': False, 'message': 'Employee not found'})

        return jsonify({
            'success': True,
            'employee': {
                'id': staff.id,
                'name': staff.name,
                'employee_id': staff.employee_id,
                'face_image_url': staff.face_image_url[:100] + '...' if staff.face_image_url and len(staff.face_image_url) > 100 else staff.face_image_url,
                'face_image_type': 'base64' if staff.face_image_url and staff.face_image_url.startswith('data:image') else 'url',
                'has_face': staff.face_image_url is not None
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================================================
# SEPARATE ADMIN FACE MANAGEMENT SYSTEM
# ============================================================================
@main.route('/api/admin-face-login-separate', methods=['POST'])
def admin_face_login_separate():
    """Admin face login - checks BOTH Staff table AND admin_faces table"""
    try:
        data = request.get_json()
        live_image_data = data.get('image_data')

        print("\n" + "="*60)
        print("👑 ADMIN FACE LOGIN (CHECKING EVERYWHERE)")
        print("="*60)
        print(f"Live image data received: {len(live_image_data) if live_image_data else 0} chars")

        if not live_image_data:
            return jsonify({
                'success': False,
                'message': 'No image data provided'
            })

        from app.services.facepp_service import FacePlusPlusService
        face_service = FacePlusPlusService()

        # ============================================
        # 1. Check admin_faces table FIRST
        # ============================================
        admin_faces = []
        import sqlite3

        print("\n🔍 Checking admin_faces table...")
        try:
            conn = sqlite3.connect('worknest_hr.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin_faces'")
            if cursor.fetchone():
                cursor.execute("SELECT * FROM admin_faces")
                admin_faces = [dict(row) for row in cursor.fetchall()]
                print(f"✅ Found {len(admin_faces)} faces in admin_faces table")
            else:
                print("❌ admin_faces table doesn't exist")

            conn.close()
        except Exception as e:
            print(f"❌ Error checking admin_faces: {e}")

        # ============================================
        # 2. Check Staff table (where /api/upload-admin-profile-photo saves)
        # ============================================
        print("\n🔍 Checking Staff table...")
        staff_with_faces = Staff.query.filter(
            Staff.face_image_url.isnot(None),
            Staff.is_active == True
        ).all()

        staff_faces = []
        for staff in staff_with_faces:
            if staff.face_image_url and staff.face_image_url.startswith('data:image'):
                staff_faces.append({
                    'type': 'staff',
                    'username': staff.employee_id,
                    'name': staff.name,
                    'image': staff.face_image_url,
                    'is_admin': staff.is_admin
                })

        print(f"✅ Found {len(staff_faces)} faces in Staff table")

        # ============================================
        # 3. Combine ALL faces to check
        # ============================================
        all_faces_to_check = []

        # Add admin_faces
        for admin_face in admin_faces:
            all_faces_to_check.append({
                'type': 'admin_faces',
                'username': admin_face['admin_username'],
                'name': admin_face['admin_username'],
                'image': admin_face['face_image'],
                'is_admin': True
            })

        # Add staff faces
        all_faces_to_check.extend(staff_faces)

        print(f"\n📊 TOTAL faces to compare: {len(all_faces_to_check)}")

        if len(all_faces_to_check) == 0:
            print("❌ No faces found anywhere!")
            return jsonify({
                'success': False,
                'message': 'No admin faces registered. Please login with username/password first and register your face from the dashboard.'
            })

        # List all faces for debugging
        for i, face in enumerate(all_faces_to_check):
            print(f"  {i+1}. {face['name']} ({face['type']}) - Admin: {face.get('is_admin', False)}")

        # ============================================
        # 4. Compare with ALL faces
        # ============================================
        best_match = None
        best_confidence = 0
        matched_info = None

        for face_info in all_faces_to_check:
            print(f"\n🔍 Comparing with: {face_info['name']} ({face_info['type']})")

            try:
                # Extract base64
                if face_info['image'].startswith('data:image'):
                    stored_base64 = face_info['image'].split(',')[1]

                    confidence, success = face_service.compare_faces(
                        live_image_data,
                        stored_base64,
                        image1_is_url=False,
                        image2_is_url=False
                    )

                    print(f"  Confidence: {confidence}%")

                    if success and confidence > best_confidence:
                        best_confidence = confidence
                        best_match = face_info
                        print(f"  ✅ Potential match!")

            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue

        print("\n" + "="*60)
        print("📊 FINAL RESULTS")
        print("="*60)

        if best_match and best_confidence >= 75:
            print(f"✅ MATCH FOUND: {best_match['name']} ({best_confidence}%)")
            print(f"   Type: {best_match['type']}, Username: {best_match['username']}")

            # Set admin session
            session['admin_logged_in'] = True

            # If matching with TEST001 in Staff table, use 'admin' as username
            if best_match['type'] == 'staff' and best_match['username'] == 'TEST001':
                session['admin_username'] = 'admin'
                session['admin_name'] = 'System Administrator'
            else:
                session['admin_username'] = best_match['username']
                session['admin_name'] = best_match['name']

            return jsonify({
                'success': True,
                'name': session['admin_name'],
                'username': session['admin_username'],
                'confidence': best_confidence,
                'message': f'Welcome Admin {session["admin_name"]}!',
                'redirect': '/admin/dashboard'
            })

        elif best_match and best_confidence >= 50:
            return jsonify({
                'success': False,
                'message': f'Low confidence match ({best_confidence}%). Please try again.',
                'confidence': best_confidence
            })

        else:
            print(f"❌ NO MATCH (best confidence: {best_confidence}%)")
            return jsonify({
                'success': False,
                'message': 'Face not recognized. Please try username/password.'
            })

    except Exception as e:
        print(f"🔥 ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@main.route('/api/admin-register-face-separate', methods=['POST'])
def admin_register_face_separate():
    """Register face for admin (separate from employees)"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Admin not logged in'})

    try:
        data = request.get_json()
        image_data = data.get('image_data')
        admin_username = session.get('admin_username')

        if not image_data:
            return jsonify({'success': False, 'message': 'No image data'})

        if not admin_username:
            return jsonify({'success': False, 'message': 'No admin username in session'})

        print("\n" + "="*60)
        print("👑 ADMIN FACE REGISTRATION (SEPARATE)")
        print("="*60)
        print(f"Admin username: {admin_username}")
        print(f"Image data length: {len(image_data)} chars")

        # Create full base64 data URL
        image_base64 = f"data:image/jpeg;base64,{image_data}"

        # Use SQLite3 directly
        import sqlite3

        try:
            conn = sqlite3.connect('worknest_hr.db')
            cursor = conn.cursor()
        except:
            # Fallback to database.db
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

        # Check if admin face already exists
        cursor.execute("SELECT id FROM admin_faces WHERE admin_username = ?", (admin_username,))
        existing = cursor.fetchone()

        if existing:
            # Update existing
            cursor.execute(
                "UPDATE admin_faces SET face_image = ? WHERE admin_username = ?",
                (image_base64, admin_username)
            )
            message = "Admin face updated successfully"
            print(f"✅ Updated existing face for {admin_username}")
        else:
            # Insert new
            cursor.execute(
                "INSERT INTO admin_faces (admin_username, face_image) VALUES (?, ?)",
                (admin_username, image_base64)
            )
            message = "Admin face registered successfully"
            print(f"✅ Registered new face for {admin_username}")

        conn.commit()

        # Verify
        cursor.execute(
            "SELECT LENGTH(face_image) as len FROM admin_faces WHERE admin_username = ?",
            (admin_username,)
        )
        saved = cursor.fetchone()

        if saved:
            print(f"✅ Face saved! Image size: {saved[0]} chars")

        conn.close()

        return jsonify({
            'success': True,
            'message': message
        })

    except Exception as e:
        print(f"❌ Error registering admin face: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@main.route('/api/admin-check-has-face')
def admin_check_has_face():
    """Check if current admin has registered face"""
    if not session.get('admin_logged_in'):
        return jsonify({'has_face': False})

    admin_username = session.get('admin_username')
    if not admin_username:
        return jsonify({'has_face': False})

    admin_face = db.execute(
        "SELECT face_image FROM admin_faces WHERE admin_username = ?",
        (admin_username,)
    ).fetchone()

    return jsonify({
        'has_face': admin_face is not None,
        'image_length': len(admin_face['face_image']) if admin_face else 0
    })


@main.route('/api/debug-admin-faces')
def debug_admin_faces():
    """Debug all admin faces"""
    try:
        from sqlalchemy import text
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT admin_username, LENGTH(face_image) as len FROM admin_faces"))
            admin_faces = [dict(row._mapping) for row in result]

        result_list = []
        for face in admin_faces:
            result_list.append({
                'username': face['admin_username'],
                'image_length': face['len']
            })

        return jsonify({
            'count': len(result_list),
            'admin_faces': result_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# ============================================================================
# CRITICAL MISSING ROUTES
# ============================================================================
@main.route('/debug/db-check')
def debug_db_check():
    """Debug endpoint to check database connections"""
    import sqlite3
    import os

    results = {}

    # Check worknest_hr.db
    if os.path.exists('worknest_hr.db'):
        try:
            conn = sqlite3.connect('worknest_hr.db')
            cursor = conn.cursor()

            # Get tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [t[0] for t in cursor.fetchall()]

            # Check admin_faces specifically
            cursor.execute("SELECT COUNT(*) FROM admin_faces")
            admin_faces_count = cursor.fetchone()[0]

            results['worknest_hr.db'] = {
                'exists': True,
                'tables': tables,
                'admin_faces_count': admin_faces_count
            }

            conn.close()
        except Exception as e:
            results['worknest_hr.db'] = {'exists': True, 'error': str(e)}
    else:
        results['worknest_hr.db'] = {'exists': False}

    # Check database.db
    if os.path.exists('database.db'):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [t[0] for t in cursor.fetchall()]

            cursor.execute("SELECT COUNT(*) FROM admin_faces")
            admin_faces_count = cursor.fetchone()[0]

            results['database.db'] = {
                'exists': True,
                'tables': tables,
                'admin_faces_count': admin_faces_count
            }

            conn.close()
        except Exception as e:
            results['database.db'] = {'exists': True, 'error': str(e)}
    else:
        results['database.db'] = {'exists': False}

    return jsonify(results)

@main.route('/api/upload-admin-profile-photo', methods=['POST'])
def upload_admin_profile_photo():
    """Upload admin profile photo"""
    try:
        data = request.get_json()
        image_data = data.get('image_data')

        print("=" * 50)
        print("📸 ADMIN PROFILE PHOTO UPLOAD REQUEST")
        print(f"Image data length: {len(image_data) if image_data else 0} chars")

        if not image_data:
            return jsonify({'success': False, 'message': 'No image data received'})

        # Get or create admin user (TEST001)
        admin_staff = Staff.query.filter_by(employee_id='TEST001').first()
        if not admin_staff:
            admin_staff = Staff(
                employee_id='TEST001',
                name='System Administrator',
                email='admin@worknest.com',
                is_admin=True,
                is_active=True,
                pin_hash=generate_password_hash('1234')
            )
            db.session.add(admin_staff)
            db.session.commit()
            print("✅ Created new admin user: TEST001")

        # Create data URL for storage
        image_url = f"data:image/jpeg;base64,{image_data}"

        # Update database
        admin_staff.face_image_url = image_url
        db.session.commit()

        print(f"✅ ADMIN PHOTO SAVED FOR: {admin_staff.name}")
        print("=" * 50)

        return jsonify({
            'success': True,
            'message': 'Admin profile photo uploaded successfully!',
            'image_url': image_url
        })

    except Exception as e:
        print(f"❌ ADMIN UPLOAD ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Upload failed: {str(e)}'}), 500


@main.route('/api/update-profile-photo', methods=['POST'])
def update_profile_photo():
    """Upload employee profile photo"""
    try:
        data = request.get_json()
        image_data = data.get('image_data')

        print("=" * 50)
        print("📸 EMPLOYEE PROFILE PHOTO UPLOAD REQUEST")
        print(f"Image data length: {len(image_data) if image_data else 0} chars")

        if not image_data:
            return jsonify({'success': False, 'message': 'No image data received'})

        # Get TEST001 as employee
        staff = Staff.query.filter_by(employee_id='TEST001').first()
        if not staff:
            return jsonify({'success': False, 'message': 'Staff not found'})

        # Create data URL for storage
        image_url = f"data:image/jpeg;base64,{image_data}"

        # Update database
        staff.face_image_url = image_url
        db.session.commit()

        print(f"✅ EMPLOYEE PHOTO SAVED FOR: {staff.name}")
        print("=" * 50)

        return jsonify({
            'success': True,
            'message': 'Profile photo updated successfully!',
            'image_url': image_url
        })

    except Exception as e:
        print(f"❌ EMPLOYEE UPLOAD ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Upload failed: {str(e)}'}), 500


@main.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })