"""
Routes for Send Student Result System
"""
from flask import Blueprint, render_template, request, jsonify, current_app
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

# ==================== API Routes ====================

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload and process student result file
    Expected file format: CSV with columns: name, email, score, subject (optional), batch (optional)
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
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:  # Excel file
                df = pd.read_excel(filepath)
            
            # Clean up temporary file
            os.remove(filepath)
            print("File successfully parsed")  # Debug log
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            print(f"Error parsing file: {str(e)}")  # Debug log
            return jsonify({'success': False, 'message': f'Error reading file: {str(e)}'}), 400

        # Strip whitespace from column names
        df.columns = df.columns.str.strip()

        # Validate required columns
        required_columns = ['name', 'email', 'score']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            return jsonify({
                'success': False,
                'message': f'Missing required columns: {", ".join(missing_columns)}. Found columns: {", ".join(df.columns.tolist())}'
            }), 400
        
        # Clean and validate data
        df = df.dropna(subset=['name', 'email', 'score'])

        # Convert score to float
        try:
            df['score'] = df['score'].astype(float)
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error converting score to number: {str(e)}'}), 400

        # Store in session for preview
        students_data = df.to_dict('records')
        
        return jsonify({
            'success': True,
            'message': f'File uploaded successfully. Found {len(students_data)} students.',
            'data': students_data
        }), 200
    
    except Exception as e:
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
        
        # Clear existing students (optional - can be changed to append)
        Student.query.delete()
        print("Cleared existing students")  # Debug log
        
        # Add new students
        for index, student_data in enumerate(students):
            try:
                student = Student(
                    student_id=student_data.get('student_id'),
                    name=student_data.get('name'),
                    email=student_data.get('email'),
                    score=float(student_data.get('score', 0)),
                    subject=student_data.get('subject'),
                    batch=student_data.get('batch'),
                    comment=student_data.get('comment')
                )
                db.session.add(student)
                print(f"Added student {index + 1}: {student_data.get('name')}")  # Debug log
            except Exception as e:
                db.session.rollback()
                print(f"Error adding student {index + 1}: {str(e)}")  # Debug log
                return jsonify({'success': False, 'message': f'Error adding student {student_data.get("name")}: {str(e)}'}), 400
        
        db.session.commit()
        print("Successfully saved all students")  # Debug log
        
        return jsonify({
            'success': True,
            'message': f'Successfully saved {len(students)} students to database'
        }), 200
    
    except Exception as e:
        db.session.rollback()
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
        
        # Send emails
        results = send_student_results(students)
        
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

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

