"""
Utility functions for Send Student Result System
"""
import os
import pandas as pd
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_csv_file(filepath):
    """
    Parse CSV file and return data as list of dictionaries
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        list: List of dictionaries with student data
    """
    try:
        df = pd.read_csv(filepath)
        return df.to_dict('records')
    except Exception as e:
        raise Exception(f"Error parsing CSV file: {str(e)}")

def parse_excel_file(filepath):
    """
    Parse Excel file and return data as list of dictionaries
    
    Args:
        filepath: Path to Excel file
    
    Returns:
        list: List of dictionaries with student data
    """
    try:
        df = pd.read_excel(filepath)
        return df.to_dict('records')
    except Exception as e:
        raise Exception(f"Error parsing Excel file: {str(e)}")

def validate_student_data(student_data):
    """
    Validate student data
    
    Args:
        student_data: Dictionary with student information
    
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['name', 'email', 'score']
    
    for field in required_fields:
        if field not in student_data or not student_data[field]:
            return False, f"Missing required field: {field}"
    
    # Validate email format
    if '@' not in student_data['email']:
        return False, f"Invalid email format: {student_data['email']}"
    
    # Validate score is numeric
    try:
        float(student_data['score'])
    except ValueError:
        return False, f"Score must be numeric: {student_data['score']}"
    
    return True, None

def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    return secure_filename(filename)

