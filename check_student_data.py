"""
Check what data is stored for students
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import Student
import json

def check_student_data():
    """Check student data structure"""
    
    app = create_app()
    
    with app.app_context():
        students = Student.query.all()
        
        print(f"Total students: {len(students)}")
        print("=" * 80)
        
        for student in students[:3]:  # Check first 3 students
            print(f"\nStudent: {student.name}")
            print(f"Email: {student.email}")
            print(f"Score: {student.score}")
            print(f"Student ID: {student.student_id}")
            print(f"Batch: {student.batch}")
            print(f"Comment: {student.comment}")
            print(f"\nExtra Data:")
            if student.extra_data:
                print(json.dumps(student.extra_data, indent=2))
            else:
                print("  No extra_data found!")
            print("-" * 80)

if __name__ == '__main__':
    check_student_data()
