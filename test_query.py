"""Test querying students to verify the fix"""
from app import app, db
from models import Student

with app.app_context():
    # Try to query a student by email (this was failing before)
    test_email = 'tola.tim@student.passerellesnumeriques.org'
    
    try:
        student = Student.query.filter_by(email=test_email).first()
        
        if student:
            print(f"[SUCCESS] Found student: {student.name}")
            print(f"  - ID: {student.id}")
            print(f"  - Student ID: {student.student_id}")
            print(f"  - Email: {student.email}")
            print(f"  - Score: {student.score}")
        else:
            print(f"[INFO] No student found with email: {test_email}")
            
        # Test querying all students
        all_students = Student.query.all()
        print(f"\n[SUCCESS] Total students in database: {len(all_students)}")
        
    except Exception as e:
        print(f"[ERROR] Query failed: {str(e)}")
        import traceback
        traceback.print_exc()
