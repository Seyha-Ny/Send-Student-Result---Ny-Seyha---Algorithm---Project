"""
Verify that column order was added to student records
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import Student

def verify_column_order():
    """Check if students have column order"""
    
    app = create_app()
    
    with app.app_context():
        students = Student.query.all()
        
        print(f"Checking {len(students)} students...")
        print("-" * 60)
        
        for student in students:
            if student.extra_data and '_column_order' in student.extra_data:
                print(f"[OK] {student.name}")
                print(f"     Columns: {', '.join(student.extra_data['_column_order'][:5])}...")
            else:
                print(f"[MISSING] {student.name} - No column order found")
        
        print("-" * 60)
        print("Verification complete!")

if __name__ == '__main__':
    verify_column_order()
