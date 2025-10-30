"""
Routes for Send Student Result System
"""
from flask import Blueprint, render_template, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import os
from datetime import datetime
from models import Student, EmailLog
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

            # Check if columns are generic (Unnamed, numbers) - file has no header row
            has_generic_columns = any(
                str(col).startswith('Unnamed') or str(col).isdigit() 
                for col in df.columns
            )
        except Exception as e:
            print(f"Error reading file: {str(e)}")  # Debug log
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'message': f'Error reading file: {str(e)}'}), 400

        # Replace NaN/None values with empty string
        df = df.fillna('')

        # Check if columns are numeric (no header row)
        if all(isinstance(col, int) for col in df.columns):
            print("File has no header row - auto-detecting columns...")
            
            # Try to auto-detect email column
            email_col = None
            for col_idx in df.columns:
                # Check if column contains email addresses
                sample_values = df[col_idx].astype(str).head(10)
                if any('@' in str(val) for val in sample_values):
                    email_col = col_idx
                    print(f"Found email in column {col_idx}")
                    break
            
            if email_col is None:
                return jsonify({
                    'success': False,
                    'message': f'❌ Could not detect email column in your file.\n\nYour file appears to have no header row.\n\nPlease add a header row with column names, including "email".'
                }), 400
            
            # Create generic column names
            new_columns = []
            for i, col in enumerate(df.columns):
                if col == email_col:
                    new_columns.append('email')
                else:
                    new_columns.append(f'col_{i}')
            
            df.columns = new_columns
            print(f"Auto-generated column names: {df.columns.tolist()}")
        else:
            # Strip whitespace from column names and convert to lowercase
            df.columns = df.columns.str.strip().str.lower()
        
        print(f"File columns: {df.columns.tolist()}")  # Debug log

        # Auto-fix common column name variations (OPTIONAL - only if columns exist)
        # 1. Combine first name and last name into name (if both exist)
        if 'first name' in df.columns and 'last name' in df.columns and 'name' not in df.columns:
            df['name'] = df['first name'].astype(str).str.strip() + ' ' + df['last name'].astype(str).str.strip()
            print("Combined 'first name' and 'last name' into 'name'")  # Debug log
        elif 'firstname' in df.columns and 'lastname' in df.columns and 'name' not in df.columns:
            df['name'] = df['firstname'].astype(str).str.strip() + ' ' + df['lastname'].astype(str).str.strip()
            print("Combined 'firstname' and 'lastname' into 'name'")  # Debug log
        
        # 2. Map common score column variations to 'score' (if score doesn't exist)
        if 'score' not in df.columns:
            score_mappings = ['total', 'total score', 'final score', 'grade score', 'marks', 'total marks']
            for old_col in score_mappings:
                if old_col in df.columns:
                    df['score'] = df[old_col]
                    print(f"Mapped '{old_col}' to 'score'")  # Debug log
                    break
        
        # 3. Map common ID variations (if student_id doesn't exist)
        if 'id' in df.columns and 'student_id' not in df.columns:
            df['student_id'] = df['id']
            print("Mapped 'id' to 'student_id'")  # Debug log
        
        # 4. Map common batch/class variations (if batch doesn't exist)
        if 'class' in df.columns and 'batch' not in df.columns:
            df['batch'] = df['class']
            print("Mapped 'class' to 'batch'")  # Debug log
        
        # 5. Map common comment variations (if comment doesn't exist)
        if 'comments' in df.columns and 'comment' not in df.columns:
            df['comment'] = df['comments']
            print("Mapped 'comments' to 'comment'")  # Debug log

        print(f"Columns after auto-mapping: {df.columns.tolist()}")  # Debug log

        # ONLY REQUIREMENT: Email column must exist
        if 'email' not in df.columns:
            return jsonify({
                'success': False,
                'message': f'❌ File must have an "email" column\n\nYour file has: {", ".join(df.columns.tolist())}\n\nPlease add an email column and upload again.'
            }), 400

        # Set default values for standard fields if they don't exist
        if 'name' not in df.columns:
            df['name'] = 'Student'  # Default name
        if 'score' not in df.columns:
            df['score'] = 0  # Default score
        
        # Define standard columns (these go in main fields)
        standard_columns = ['name', 'email', 'score', 'student_id', 'subject', 'batch', 'comment']
        
        # All other columns will be stored in extra_data
        print(f"All columns in file: {df.columns.tolist()}")  # Debug log

        # Clean and validate data
        # First, replace empty strings with NaN
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        
        # Only keep rows that have email (the only truly required field)
        df = df.dropna(subset=['email'])
        print(f"Rows after removing rows without email: {len(df)}")  # Debug log

        # Convert score to float if it exists, handling any non-numeric values
        if 'score' in df.columns:
            try:
                df['score'] = pd.to_numeric(df['score'], errors='coerce')
                # Fill NaN scores with 0
                df['score'] = df['score'].fillna(0)
                print(f"Scores converted successfully")  # Debug log
            except Exception as e:
                print(f"Error converting score: {str(e)}")  # Debug log
                df['score'] = 0

        # Only add required fields if they don't exist (minimal defaults)
        if 'name' not in df.columns:
            df['name'] = ''  # Empty, will be hidden in email
        if 'score' not in df.columns:
            df['score'] = ''  # Empty, will be hidden in email

        # Store original column order
        original_columns = df.columns.tolist()
        print(f"Original column order: {original_columns}")  # Debug log
        
        # Convert DataFrame to records, handling NaN values
        df = df.fillna('')  # Replace NaN with empty string
        students_data = df.to_dict('records')

        # Clean up the data for JSON serialization
        clean_data = []
        for student in students_data:
            clean_student = {}
            extra_data = {}  # Store extra columns here - PRESERVE ORDER
            extra_columns_order = []  # Track the order of extra columns
            
            # Process columns in original file order
            for key in original_columns:
                if key not in student:
                    continue
                    
                value = student[key]
                
                # Handle various types of missing/invalid values
                if value is None or (isinstance(value, float) and pd.isna(value)):
                    processed_value = None
                elif isinstance(value, str) and value.strip() == '':
                    processed_value = None
                elif isinstance(value, float):
                    # Convert float to int if it's a whole number
                    if value == int(value):
                        processed_value = int(value)
                    else:
                        processed_value = float(value)
                else:
                    # Convert to string to ensure JSON serialization
                    processed_value = str(value).strip() if value else None
                
                # Separate standard columns from extra columns
                if key in standard_columns:
                    clean_student[key] = processed_value
                else:
                    # Store in extra_data IN ORDER
                    if processed_value is not None:
                        extra_data[key] = processed_value
                        extra_columns_order.append(key)
            
            # Add extra_data to student record if there are any extra columns
            if extra_data:
                # Store the column order as a special key
                extra_data['_column_order'] = extra_columns_order
                clean_student['extra_data'] = extra_data
            
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

@api_bp.route('/download-sample', methods=['GET'])
def download_sample():
    """
    Download sample CSV file for students data
    """
    try:
        # Get the base directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sample_file = os.path.join(base_dir, 'sample_students.csv')
        
        # Check if sample file exists
        if not os.path.exists(sample_file):
            return jsonify({'success': False, 'message': 'Sample file not found'}), 404
        
        # Send file for download
        return send_file(
            sample_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name='sample_students.csv'
        )
    
    except Exception as e:
        print(f"Error downloading sample: {str(e)}")  # Debug log
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

        # Handle special case: combining first name and last name into name
        if 'first name' in mapping and 'last name' in mapping:
            if mapping['first name'] == 'name' and mapping['last name'] == 'name':
                # Combine first name and last name
                df['name'] = df['first name'].astype(str) + ' ' + df['last name'].astype(str)
                # Remove the original columns from mapping
                mapping = {k: v for k, v in mapping.items() if k not in ['first name', 'last name']}
        
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
                    student.student_id = student_data.get('student_id')
                    student.name = student_data.get('name')
                    student.score = float(student_data.get('score', 0))
                    student.subject = student_data.get('subject')
                    student.batch = student_data.get('batch')
                    student.comment = student_data.get('comment')
                    student.extra_data = student_data.get('extra_data')  # Store all extra columns
                    
                    # Sync comment to extra_data so it appears in emails
                    if student.extra_data is None:
                        student.extra_data = {}
                    if student.comment:
                        student.extra_data['comment'] = student.comment
                    elif 'comment' in student.extra_data:
                        del student.extra_data['comment']
                    
                    student.updated_at = datetime.utcnow()
                    updated_count += 1
                    print(f"Updating student: {email}")  # Debug log
                else:
                    # Add new student
                    extra_data = student_data.get('extra_data') or {}
                    comment = student_data.get('comment')
                    
                    # Sync comment to extra_data so it appears in emails
                    if comment:
                        extra_data['comment'] = comment
                    
                    student = Student(
                        student_id=student_data.get('student_id'),
                        name=student_data.get('name'),
                        email=email,
                        score=float(student_data.get('score', 0)),
                        subject=student_data.get('subject'),
                        batch=student_data.get('batch'),
                        comment=comment,
                        extra_data=extra_data  # Store all extra columns including comment
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
        student.updated_at = datetime.now()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comment updated successfully',
            'data': student.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update any student field"""
    try:
        data = request.get_json()
        
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        # Update allowed fields
        allowed_fields = ['name', 'email', 'score', 'student_id', 'subject', 'batch', 'comment']
        
        for field, value in data.items():
            if field in allowed_fields:
                if field == 'score':
                    # Convert score to float
                    try:
                        value = float(value) if value else 0.0
                    except (ValueError, TypeError):
                        return jsonify({'success': False, 'message': 'Invalid score value'}), 400
                
                setattr(student, field, value)
                
                # Sync comment to extra_data so it appears in emails
                if field == 'comment':
                    if student.extra_data is None:
                        student.extra_data = {}
                    if value:
                        student.extra_data['comment'] = value
                    elif 'comment' in student.extra_data:
                        del student.extra_data['comment']
                    # Mark extra_data as modified for SQLAlchemy to detect the change
                    from sqlalchemy.orm.attributes import flag_modified
                    flag_modified(student, 'extra_data')
        
        student.updated_at = datetime.now()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student updated successfully',
            'data': student.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/clear-students', methods=['DELETE'])
def clear_students():
    """Clear all student data and email logs from database"""
    try:
        # Delete all email logs first (due to foreign key constraint)
        email_logs_count = EmailLog.query.delete()
        
        # Delete all students
        students_count = Student.query.delete()
        
        # Commit the changes
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully deleted {students_count} students and {email_logs_count} email logs'
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing students: {str(e)}")  # Debug log
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

@api_bp.route('/test-email-config', methods=['POST'])
def test_email_config():
    """Test email configuration with provided credentials"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
        # Test email configuration by temporarily updating Flask-Mail config
        from flask_mail import Message
        import smtplib
        
        # Test SMTP connection
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            server.quit()
            
            return jsonify({
                'success': True,
                'message': 'Email configuration is valid'
            }), 200
            
        except smtplib.SMTPAuthenticationError:
            return jsonify({
                'success': False,
                'message': 'Authentication failed. Please check your email and app password.'
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'SMTP connection failed: {str(e)}'
            }), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@api_bp.route('/send-results', methods=['POST'])
def send_results_with_config():
    """Send results to students using sender's email credentials (REQUIRED)."""
    try:
        data = request.get_json() or {}
        email_config = data.get('email_config', {}) or {}
        student_ids = data.get('student_ids', [])

        # REQUIRE sender credentials
        sender_email = email_config.get('email')
        sender_password = email_config.get('password')
        
        if not sender_email or not sender_password:
            return jsonify({
                'success': False, 
                'message': 'Sender email and password are required. Please enter your Gmail credentials first.'
            }), 400

        # Determine recipients
        if not student_ids:
            students = Student.query.all()
        else:
            students = Student.query.filter(Student.id.in_(student_ids)).all()

        if not students:
            return jsonify({'success': False, 'message': 'No students found'}), 404

        # Temporarily switch mail config to use sender's credentials
        original_username = current_app.config.get('MAIL_USERNAME')
        original_password = current_app.config.get('MAIL_PASSWORD')
        original_sender = current_app.config.get('MAIL_DEFAULT_SENDER')

        current_app.config['MAIL_USERNAME'] = sender_email
        current_app.config['MAIL_PASSWORD'] = sender_password
        current_app.config['MAIL_DEFAULT_SENDER'] = sender_email
        mail.init_app(current_app)

        try:
            # Send emails using sender's email as FROM address
            # Owner email can receive BCC if configured
            owner_email = current_app.config.get('MAIL_OWNER_EMAIL')
            results = send_student_results(students, owner_email)
            return jsonify({
                'success': True, 
                'message': f'Emails sent from {sender_email}', 
                'results': results
            }), 200
        finally:
            # Restore original configuration
            current_app.config['MAIL_USERNAME'] = original_username
            current_app.config['MAIL_PASSWORD'] = original_password
            current_app.config['MAIL_DEFAULT_SENDER'] = original_sender
            mail.init_app(current_app)

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ==================== Help & FAQ APIs ====================

@api_bp.route('/help-faqs', methods=['GET'])
def get_help_faqs():
    faqs = [
        {
            'q': 'What file formats are supported?',
            'a': 'CSV (.csv) and Excel (.xlsx, .xls) files are supported.'
        },
        {
            'q': 'How to send using my own Gmail as sender?',
            'a': 'Enter your Gmail and App Password on the home page, test configuration, then click Send Results Now.'
        },
        {
            'q': 'Gmail authentication failed',
            'a': 'Use a Gmail App Password (requires 2-Step Verification). Generate at https://myaccount.google.com/apppasswords.'
        },
        {
            'q': 'Emails go to spam',
            'a': 'Ask recipients to mark as Not Spam, avoid spammy content, and use a domain with SPF/DKIM if possible.'
        },
        {
            'q': 'Rate limits or too many failures',
            'a': 'Send in smaller batches, verify email addresses, and retry later if rate-limited.'
        },
        {
            'q': 'Receive copies of sent emails',
            'a': 'Set MAIL_OWNER_EMAIL in the environment to receive BCC copies.'
        }
    ]
    return jsonify({'success': True, 'data': faqs}), 200

@api_bp.route('/help-question', methods=['POST'])
def answer_help_question():
    try:
        data = request.get_json() or {}
        query = (data.get('query') or '').strip().lower()
        if not query:
            return jsonify({'success': False, 'message': 'Query is required'}), 400

        faqs = [
            ('file formats supported', 'CSV (.csv) and Excel (.xlsx, .xls) files are supported.'),
            ('send using my own gmail', 'Enter your Gmail and App Password on the home page, test configuration, then click Send Results Now.'),
            ('gmail authentication failed', 'Use a Gmail App Password (requires 2-Step Verification). Generate at https://myaccount.google.com/apppasswords.'),
            ('emails spam', 'Ask recipients to mark as Not Spam, avoid spammy content, and use a domain with SPF/DKIM if possible.'),
            ('rate limit failure', 'Send in smaller batches, verify email addresses, and retry later if rate-limited.'),
            ('bcc owner copy', 'Set MAIL_OWNER_EMAIL in the environment to receive BCC copies.'),
        ]

        # Simple keyword scoring
        best = None
        best_score = 0
        for key, ans in faqs:
            score = 0
            for token in key.split():
                if token in query:
                    score += 1
            if score > best_score:
                best_score = score
                best = (key, ans)

        if best and best_score > 0:
            return jsonify({'success': True, 'answer': best[1]}), 200
        else:
            return jsonify({'success': True, 'answer': 'Please check the Help page FAQs and Troubleshooting. If the issue persists, verify your file format and email configuration.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200