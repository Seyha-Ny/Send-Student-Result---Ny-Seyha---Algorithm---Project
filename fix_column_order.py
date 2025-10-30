"""
Migration script to add column order to existing student records
Run this once to fix existing data in the database
"""
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import Student
from extensions import db

def fix_column_order():
    """Add _column_order to existing student records"""
    
    app = create_app()
    
    with app.app_context():
        # Define the correct column order from your CSV file
        correct_order = [
            'first name',
            'last name', 
            'id',
            'class',
            'hw1',
            'participation',
            'q1',
            'final khmer',
            'final english',
            'total',
            'grade',
            'comments'
        ]
        
        # Get all students
        students = Student.query.all()
        
        print(f"Found {len(students)} students in database")
        
        updated_count = 0
        
        for student in students:
            if student.extra_data:
                # Check if _column_order already exists
                if '_column_order' not in student.extra_data:
                    # Build the column order based on what fields exist in extra_data
                    column_order = []
                    for col in correct_order:
                        if col in student.extra_data:
                            column_order.append(col)
                    
                    # Add the _column_order key
                    student.extra_data['_column_order'] = column_order
                    
                    # Mark the field as modified so SQLAlchemy knows to update it
                    from sqlalchemy.orm.attributes import flag_modified
                    flag_modified(student, 'extra_data')
                    
                    updated_count += 1
                    
                    print(f"Updated student: {student.name} (ID: {student.id})")
                    print(f"  Column order: {column_order}")
        
        # Commit all changes
        if updated_count > 0:
            db.session.commit()
            print(f"\nSuccessfully updated {updated_count} student records!")
        else:
            print("\nAll records already have column order information!")
        
        return updated_count

if __name__ == '__main__':
    print("=" * 60)
    print("COLUMN ORDER MIGRATION SCRIPT")
    print("=" * 60)
    print("\nThis script will add column order information to existing")
    print("student records in the database.\n")
    
    try:
        updated = fix_column_order()
        print("\n" + "=" * 60)
        print("MIGRATION COMPLETE")
        print("=" * 60)
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
