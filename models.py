"""
Database models for Student Results System
"""
from datetime import datetime
from extensions import db
import pytz

# Define Bangkok timezone
BANGKOK_TZ = pytz.timezone('Asia/Bangkok')

def get_bangkok_time():
    """Get current time in Bangkok timezone"""
    return datetime.now(BANGKOK_TZ)

class Student(db.Model):
    """Student model to store student information and results"""
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50))
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    score = db.Column(db.Float, nullable=False)
    subject = db.Column(db.String(120))
    batch = db.Column(db.String(50))
    comment = db.Column(db.Text)
    extra_data = db.Column(db.JSON)  # Store all additional columns from uploaded file
    created_at = db.Column(db.DateTime, default=get_bangkok_time)
    updated_at = db.Column(db.DateTime, default=get_bangkok_time, onupdate=get_bangkok_time)

    def to_dict(self):
        """Convert student object to dictionary"""
        result = {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'score': self.score,
            'subject': self.subject,
            'batch': self.batch,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        # Include extra_data if it exists
        if self.extra_data:
            result['extra_data'] = self.extra_data
        return result

class EmailLog(db.Model):
    """Email log model to track email sending status"""
    __tablename__ = 'email_logs'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    error_message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=get_bangkok_time)

    def to_dict(self):
        """Convert email log object to dictionary"""
        student = Student.query.get(self.student_id)
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': student.name if student else 'Unknown',
            'student_email': student.email if student else 'Unknown',
            'status': self.status,
            'error_message': self.error_message,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SharedResult(db.Model):
    """Shared result model for sharing student results via secure links"""
    __tablename__ = 'shared_results'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    share_token = db.Column(db.String(100), unique=True, nullable=False)
    shared_with_email = db.Column(db.String(120), nullable=False)
    shared_by = db.Column(db.String(120))
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=get_bangkok_time)
    last_viewed_at = db.Column(db.DateTime)

    def to_dict(self):
        """Convert shared result object to dictionary"""
        student = Student.query.get(self.student_id)
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': student.name if student else 'Unknown',
            'student_email': student.email if student else 'Unknown',
            'share_token': self.share_token,
            'shared_with_email': self.shared_with_email,
            'shared_by': self.shared_by,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_viewed_at': self.last_viewed_at.isoformat() if self.last_viewed_at else None
        }

"""
Routes for Send Student Result System
"""
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import pandas as pd
import os
import uuid
from datetime import datetime, timedelta
from models import Student, EmailLog, SharedResult
from extensions import db, mail
from email_service import send_student_results, send_email_to_student
from utils import allowed_file, parse_csv_file

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# ==================== Frontend Routes ====================

@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main_bp.route('/preview')
def preview():
    """Preview page for uploaded data"""
    return render_template('preview.html')

@main_bp.route('/logs')
def logs():
    """Email logs page"""
    return render_template('logs.html')

@main_bp.route('/help')
def help():
    """Help and documentation page"""
    return render_template('help.html')

@main_bp.route('/share/<token>')
def shared_results(token):
    """Shared results page"""
    return render_template('shared_results.html', token=token)

# ==================== API Routes ====================

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload and process student result file
    Handles files with extra fields (removes them) and missing fields (returns for manual entry)
    Expected file format: CSV/Excel with columns: name, email, score, subject (optional), batch (optional)
    """
    try:
        print("Upload request received")  # Debug log

        # Check if the post request has the file part
        if 'file' not in request.files:
            print("No file part in request")  # Debug log
            return jsonify({'success': False, 'message': 'No file provided'}), 400

        file = request.files['file']
        print(f"File received: {file.filename}")  # Debug log

        if file.filename == '':
            print("No selected file")  # Debug log
            return jsonify({'success': False, 'message': 'No file selected'}), 400

        if not allowed_file(file.filename):
            print(f"Invalid file type: {file.filename}")  # Debug log
            return jsonify({'success': False, 'message': 'Invalid file format. Only CSV and Excel files are allowed'}), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File saved to: {filepath}")  # Debug log

        # Parse file
        try:
            print(f"Attempting to parse file: {filename}")  # Debug log
            if filename.endswith('.csv'):
                print("Parsing as CSV file")  # Debug log
                df = pd.read_csv(filepath, na_values=['', 'NaN', 'nan', 'NA', 'null'], keep_default_na=True)
            elif filename.endswith(('.xlsx', '.xls')):
                print("Parsing as Excel file")  # Debug log
                try:
                    # Try reading with openpyxl engine first (for .xlsx)
                    df = pd.read_excel(filepath, engine='openpyxl', na_values=['', 'NaN', 'nan', 'NA', 'null'], keep_default_na=True)
                except Exception as xlsx_error:
                    print(f"openpyxl failed, trying xlrd: {str(xlsx_error)}")  # Debug log
                    # Fallback to xlrd for older Excel files
                    try:
                        df = pd.read_excel(filepath, engine='xlrd', na_values=['', 'NaN', 'nan', 'NA', 'null'], keep_default_na=True)
                    except Exception as xlrd_error:
                        print(f"xlrd also failed: {str(xlrd_error)}")  # Debug log
                        # Final fallback - let pandas auto-detect
                        df = pd.read_excel(filepath, na_values=['', 'NaN', 'nan', 'NA', 'null'], keep_default_na=True)
            else:
                raise ValueError(f"Unsupported file format: {filename}")

            # Check if the file has no headers (all columns are numeric or first row looks like data)
            # If first row contains data instead of headers, use it as header
            if len(df) > 0:
                first_row = df.iloc[0]
                # Check if first row looks like data (contains email, numbers, etc.)
                has_email = any('@' in str(val) for val in first_row if pd.notna(val))
                has_numeric = any(
                    isinstance(val, (int, float)) or
                    (isinstance(val, str) and val.strip() and val.strip().replace('.', '', 1).replace('-', '', 1).isdigit())
                    for val in first_row if pd.notna(val)
                )

                if has_email or has_numeric:
                    print("First row appears to be data, using it as header")  # Debug log
                    # Use first row as header
                    new_header = [str(val).strip() if pd.notna(val) else f'col_{i}' for i, val in enumerate(first_row)]
                    df = df[1:]
                    df.columns = new_header
                    df = df.reset_index(drop=True)

            # Clean up temporary file
            os.remove(filepath)
            print("File successfully parsed")  # Debug log
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            print(f"Error parsing file: {str(e)}")  # Debug log
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'message': f'Error reading file: {str(e)}'}), 400

        # Replace NaN/None values with empty string
        df = df.fillna('')

        # Strip whitespace from column names and convert to lowercase
        df.columns = df.columns.str.strip().str.lower()
        print(f"File columns: {df.columns.tolist()}")  # Debug log

        # Define required and optional columns
        required_columns = ['name', 'email', 'score']
        optional_columns = ['student_id', 'subject', 'batch', 'comment']
        all_allowed_columns = required_columns + optional_columns

        # Check for missing required columns
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            # Return file data with missing columns for manual entry
            print(f"Missing columns: {missing_columns}")  # Debug log
            return jsonify({
                'success': False,
                'has_missing_fields': True,
                'missing_columns': missing_columns,
                'found_columns': df.columns.tolist(),
                'message': f'Missing required columns: {", ".join(missing_columns)}. Please map the columns manually.',
                'data': df.to_dict('records'),
                'row_count': len(df)
            }), 200

        # Remove extra columns (keep only allowed columns)
        columns_to_keep = [col for col in df.columns if col in all_allowed_columns]
        df = df[columns_to_keep]
        print(f"Kept columns: {columns_to_keep}")  # Debug log

        # Clean and validate data
        # First, replace empty strings with NaN
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        
        # Remove rows with missing required fields
        df = df.dropna(subset=['name', 'email', 'score'])
        print(f"Rows after removing NaN: {len(df)}")  # Debug log

        # Convert score to float, handling any non-numeric values
        try:
            df['score'] = pd.to_numeric(df['score'], errors='coerce')
            # Drop rows where score conversion failed
            df = df.dropna(subset=['score'])
            print(f"Rows after score conversion: {len(df)}")  # Debug log
        except Exception as e:
            print(f"Error converting score: {str(e)}")  # Debug log
            return jsonify({'success': False, 'message': f'Error converting scores to numbers: {str(e)}'}), 400

        # Fill optional columns with None if not present
        for col in optional_columns:
            if col not in df.columns:
                df[col] = None

        # Convert DataFrame to records, handling NaN values
        df = df.fillna('')  # Replace NaN with empty string
        students_data = df.to_dict('records')

        # Clean up the data for JSON serialization
        clean_data = []
        for student in students_data:
            clean_student = {}
            for key, value in student.items():
                # Handle various types of missing/invalid values
                if value is None or (isinstance(value, float) and pd.isna(value)):
                    clean_student[key] = None
                elif isinstance(value, str) and value.strip() == '':
                    clean_student[key] = None
                elif isinstance(value, float):
                    # Convert float to int if it's a whole number
                    if value == int(value):
                        clean_student[key] = int(value)
                    else:
                        clean_student[key] = float(value)
                else:
                    # Convert to string to ensure JSON serialization
                    clean_student[key] = str(value).strip() if value else None
            clean_data.append(clean_student)

        return jsonify({
            'success': True,
            'has_missing_fields': False,
            'message': f'File uploaded successfully. Found {len(clean_data)} students.',
            'data': clean_data
        }), 200

    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug log
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/map-columns', methods=['POST'])
def map_columns():
    """
    Handle manual column mapping for files with missing required fields
    Expects: { data: [...], mapping: { 'column_name': 'required_field' } }
    """
    try:
        print("Column mapping request received")  # Debug log

        if not request.is_json:
            return jsonify({'success': False, 'message': 'Invalid request format. Expected JSON'}), 400

        data = request.get_json()
        file_data = data.get('data', [])
        mapping = data.get('mapping', {})

        print(f"Received {len(file_data)} rows and mapping: {mapping}")  # Debug log

        if not file_data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        if not mapping:
            return jsonify({'success': False, 'message': 'No column mapping provided'}), 400

        # Create DataFrame from file data
        df = pd.DataFrame(file_data)

        # Apply mapping - rename columns according to mapping
        df = df.rename(columns=mapping)

        # Define required columns
        required_columns = ['name', 'email', 'score']
        optional_columns = ['student_id', 'subject', 'batch', 'comment']

        # Verify all required columns are now present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({
                'success': False,
                'message': f'Mapping incomplete. Still missing: {", ".join(missing_columns)}'
            }), 400

        # Replace NaN/None values with empty string first
        df = df.fillna('')

        # Remove rows with missing required fields
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        df = df.dropna(subset=['name', 'email', 'score'])

        # Convert score to float, handling any non-numeric values
        try:
            df['score'] = pd.to_numeric(df['score'], errors='coerce')
            # Drop rows where score conversion failed
            df = df.dropna(subset=['score'])
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error converting score to number: {str(e)}'}), 400

        # Keep only allowed columns
        all_allowed_columns = required_columns + optional_columns
        columns_to_keep = [col for col in df.columns if col in all_allowed_columns]
        df = df[columns_to_keep]

        # Fill optional columns with None if not present
        for col in optional_columns:
            if col not in df.columns:
                df[col] = None

        # Convert DataFrame to records, handling NaN values
        df = df.fillna('')  # Replace NaN with empty string
        students_data = df.to_dict('records')

        # Clean up the data for JSON serialization
        clean_data = []
        for student in students_data:
            clean_student = {}
            for key, value in student.items():
                # Handle various types of missing/invalid values
                if value is None or (isinstance(value, float) and pd.isna(value)):
                    clean_student[key] = None
                elif isinstance(value, str) and value.strip() == '':
                    clean_student[key] = None
                elif isinstance(value, float):
                    # Convert float to int if it's a whole number
                    if value == int(value):
                        clean_student[key] = int(value)
                    else:
                        clean_student[key] = float(value)
                else:
                    # Convert to string to ensure JSON serialization
                    clean_student[key] = str(value).strip() if value else None
            clean_data.append(clean_student)

        print(f"Successfully mapped {len(clean_data)} students")  # Debug log

        return jsonify({
            'success': True,
            'message': f'Column mapping successful. Found {len(clean_data)} students.',
            'data': clean_data
        }), 200

    except Exception as e:
        print(f"Error in column mapping: {str(e)}")  # Debug log
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/save-students', methods=['POST'])
def save_students():
    """Save student data to database"""
    try:
        print("Save students request received")  # Debug log

        if not request.is_json:
            print("Request is not JSON")  # Debug log
            return jsonify({'success': False, 'message': 'Invalid request format. Expected JSON'}), 400

        data = request.get_json()
        students = data.get('students', [])

        print(f"Received {len(students)} students")  # Debug log

        if not students:
            print("No students data provided")  # Debug log
            return jsonify({'success': False, 'message': 'No students provided'}), 400

        saved_count = 0
        updated_count = 0

        for student_data in students:
            try:
                email = student_data.get('email')
                if not email:
                    continue

                student = Student.query.filter_by(email=email).first()

                if student:
                    # Update existing student
                    student.name = student_data.get('name')
                    student.score = float(student_data.get('score', 0))
                    student.subject = student_data.get('subject')
                    student.batch = student_data.get('batch')
                    student.comment = student_data.get('comment')
                    student.updated_at = get_bangkok_time()
                    updated_count += 1
                    print(f"Updating student: {email}")  # Debug log
                else:
                    # Add new student
                    student = Student(
                        name=student_data.get('name'),
                        email=email,
                        score=float(student_data.get('score', 0)),
                        subject=student_data.get('subject'),
                        batch=student_data.get('batch'),
                        comment=student_data.get('comment')
                    )
                    db.session.add(student)
                    saved_count += 1
                    print(f"Adding new student: {email}")  # Debug log

            except Exception as e:
                db.session.rollback()
                print(f"Error processing student {student_data.get('email')}: {str(e)}")  # Debug log
                return jsonify({'success': False, 'message': f'Error processing student {student_data.get("name")}: {str(e)}'}), 400

        db.session.commit()
        print(f"Successfully saved {saved_count} and updated {updated_count} students")  # Debug log

        return jsonify({
            'success': True,
            'message': f'Successfully saved {saved_count} and updated {updated_count} students to the database'
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error saving students: {str(e)}")  # Debug log
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@api_bp.route('/students', methods=['GET'])
def get_students():
    """Get all students from database"""
    try:
        students = Student.query.all()
        return jsonify({
            'success': True,
            'data': [student.to_dict() for student in students]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/send-results', methods=['POST'])
def send_results():
    """Send results to all students via email"""
    try:
        data = request.get_json()
        student_ids = data.get('student_ids', [])
        
        if not student_ids:
            # Send to all students
            students = Student.query.all()
        else:
            students = Student.query.filter(Student.id.in_(student_ids)).all()
        
        if not students:
            return jsonify({'success': False, 'message': 'No students found'}), 404
        
        owner_email = current_app.config.get('MAIL_OWNER_EMAIL')
        
        # Send emails
        results = send_student_results(students, owner_email)
        
        return jsonify({
            'success': True,
            'message': f'Email sending process completed',
            'results': results
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/email-logs', methods=['GET'])
def get_email_logs():
    """Get email sending logs"""
    try:
        logs = EmailLog.query.order_by(EmailLog.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [log.to_dict() for log in logs]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/email-logs/export', methods=['GET'])
def export_logs():
    """Export email logs as CSV"""
    try:
        logs = EmailLog.query.all()
        
        if not logs:
            return jsonify({'success': False, 'message': 'No logs to export'}), 404
        
        # Create DataFrame
        data = [log.to_dict() for log in logs]
        df = pd.DataFrame(data)
        
        # Save to CSV
        filename = f'email_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        df.to_csv(filepath, index=False)
        
        return jsonify({
            'success': True,
            'message': 'Logs exported successfully',
            'filename': filename
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ==================== Sharing Routes ====================

@api_bp.route('/share/create', methods=['POST'])
def create_share():
    """Create a shareable link for student results"""
    try:
        data = request.get_json()
        student_ids = data.get('student_ids', [])
        shared_with_email = data.get('shared_with_email')
        shared_by = data.get('shared_by', 'admin')
        expires_in_days = data.get('expires_in_days', 30)
        
        if not student_ids:
            return jsonify({'success': False, 'message': 'No students selected'}), 400
        
        if not shared_with_email:
            return jsonify({'success': False, 'message': 'Recipient email is required'}), 400
        
        # Get students
        students = Student.query.filter(Student.id.in_(student_ids)).all()
        if not students:
            return jsonify({'success': False, 'message': 'No students found'}), 404
        
        # Generate unique token
        share_token = str(uuid.uuid4())
        
        # Calculate expiration date
        expires_at = get_bangkok_time() + timedelta(days=expires_in_days)
        
        # Create shared result
        shared_result = SharedResult(
            student_id=student_ids[0] if len(student_ids) == 1 else None,  # For single student
            share_token=share_token,
            shared_with_email=shared_with_email,
            shared_by=shared_by,
            expires_at=expires_at,
            is_active=True
        )
        
        db.session.add(shared_result)
        db.session.commit()
        
        # Generate share URL
        base_url = request.host_url.rstrip('/')
        share_url = f"{base_url}/share/{share_token}"
        
        return jsonify({
            'success': True,
            'message': 'Share link created successfully',
            'share_url': share_url,
            'share_token': share_token,
            'expires_at': expires_at.isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/share/<token>', methods=['GET'])
def get_shared_results(token):
    """Get shared student results"""
    try:
        # Find active shared result
        shared_result = SharedResult.query.filter_by(
            share_token=token,
            is_active=True
        ).first()
        
        if not shared_result:
            return jsonify({'success': False, 'message': 'Invalid or expired share link'}), 404
        
        # Check if expired
        if get_bangkok_time() > shared_result.expires_at:
            shared_result.is_active = False
            db.session.commit()
            return jsonify({'success': False, 'message': 'Share link has expired'}), 410
        
        # Get students
        if shared_result.student_id:
            # Single student share
            students = Student.query.filter_by(id=shared_result.student_id).all()
        else:
            # Multiple students share - get all students from the original selection
            # For now, return all students (you might want to store the full list in the future)
            students = Student.query.all()
        
        if not students:
            return jsonify({'success': False, 'message': 'No student data found'}), 404
        
        # Update view count and last viewed time
        shared_result.view_count += 1
        shared_result.last_viewed_at = get_bangkok_time()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'students': [student.to_dict() for student in students],
                'shared_by': shared_result.shared_by,
                'shared_with': shared_result.shared_with_email,
                'expires_at': shared_result.expires_at.isoformat(),
                'view_count': shared_result.view_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/share/<token>/deactivate', methods=['POST'])
def deactivate_share(token):
    """Deactivate a share link"""
    try:
        shared_result = SharedResult.query.filter_by(share_token=token).first()
        
        if not shared_result:
            return jsonify({'success': False, 'message': 'Share link not found'}), 404
        
        shared_result.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Share link deactivated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/shares', methods=['GET'])
def get_all_shares():
    """Get all active share links"""
    try:
        shares = SharedResult.query.filter_by(is_active=True).order_by(SharedResult.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [share.to_dict() for share in shares]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/students/<int:student_id>/comment', methods=['PUT'])
def update_student_comment(student_id):
    """Update student comment"""
    try:
        data = request.get_json()
        comment = data.get('comment', '')
        
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        student.comment = comment
        
        # Sync comment to extra_data so it appears in emails
        if student.extra_data is None:
            student.extra_data = {}
        if comment:
            student.extra_data['comment'] = comment
        elif 'comment' in student.extra_data:
            del student.extra_data['comment']
        
        student.updated_at = get_bangkok_time()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comment updated successfully',
            'data': student.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200