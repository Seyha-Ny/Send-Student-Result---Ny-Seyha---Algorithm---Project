"""
Test email generation to see what fields are included
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import Student
from email_service import get_auto_comment

def test_email_fields():
    """Test what fields will be shown in email"""
    
    app = create_app()
    
    with app.app_context():
        # Get first student (Seyha Ny)
        student = Student.query.filter_by(name='Seyha Ny').first()
        
        if not student:
            print("Student not found!")
            return
        
        print(f"Testing email for: {student.name}")
        print(f"Score: {student.score}")
        print("=" * 80)
        
        # Simulate the email generation logic
        all_fields = []
        has_comment = False
        
        if student.extra_data:
            if '_column_order' in student.extra_data:
                column_order = student.extra_data['_column_order']
                print(f"\nColumn order: {column_order}\n")
                
                for key in column_order:
                    if key in student.extra_data and key != '_column_order':
                        value = student.extra_data[key]
                        
                        # Auto-generate comment if empty
                        if key.lower() in ['comment', 'comments']:
                            has_comment = True
                            if not value or str(value).strip() in ['', 'N/A', 'None', 'nan', 'NaN']:
                                value = get_auto_comment(student.score)
                        
                        # Include ALL fields
                        if value is not None and str(value).strip() not in ['N/A', 'None', 'nan', 'NaN']:
                            display_value = str(value) if value != '' else ''
                            if display_value:
                                all_fields.append((key, display_value))
                                print(f"[OK] {key.upper():20} = {display_value}")
        
        if not has_comment:
            auto_comment = get_auto_comment(student.score)
            all_fields.append(('comments', auto_comment))
            print(f"[OK] {'COMMENTS (AUTO)':20} = {auto_comment}")
        
        print("\n" + "=" * 80)
        print(f"Total fields to display: {len(all_fields)}")
        print("=" * 80)
        
        # Show table structure
        print("\nEmail table will show:")
        print(" | ".join([key.upper() for key, _ in all_fields]))

if __name__ == '__main__':
    test_email_fields()
