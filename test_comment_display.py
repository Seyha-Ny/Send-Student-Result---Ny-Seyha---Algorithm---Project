"""
Test that comments are displayed in the email
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import Student

def test_comment_display():
    """Test that comment field is included in email"""
    
    app = create_app()
    
    with app.app_context():
        # Get a student
        student = Student.query.first()
        
        if not student:
            print("No students found in database!")
            return
        
        print(f"Testing comment display for: {student.name}")
        print(f"Score: {student.score}")
        print("=" * 80)
        
        # Check comment field
        print(f"\nDirect comment field: {student.comment}")
        
        # Check extra_data
        if student.extra_data:
            print(f"Extra data comment: {student.extra_data.get('comment', 'Not found')}")
        
        # Simulate the email generation logic
        all_fields = []
        
        # Add FIRST NAME and LAST NAME first
        if student.extra_data and 'first_name' in student.extra_data:
            all_fields.append(('FIRST NAME', student.extra_data['first_name']))
        if student.extra_data and 'last_name' in student.extra_data:
            all_fields.append(('LAST NAME', student.extra_data['last_name']))
        
        # Add subjects
        if student.extra_data:
            subject_scores = {}
            for key in sorted(student.extra_data.keys()):
                if key.startswith('subject_'):
                    try:
                        num = key.split('_')[1]
                        subject_name = student.extra_data.get(f'subject_{num}', '')
                        subject_score = student.extra_data.get(f'score_{num}', '')
                        
                        if subject_name and str(subject_name).strip() not in ['', 'N/A', 'None', 'nan', 'NaN']:
                            subject_scores[num] = {
                                'name': str(subject_name),
                                'score': str(subject_score) if subject_score else '0'
                            }
                    except:
                        continue
            
            for num in sorted(subject_scores.keys(), key=lambda x: int(x)):
                subject_data = subject_scores[num]
                all_fields.append((subject_data['name'].upper(), subject_data['score']))
        
        # Add TOTAL
        if student.score is not None:
            all_fields.append(('TOTAL', str(student.score)))
        
        # Add GRADE
        if student.extra_data and 'grade' in student.extra_data:
            grade_value = student.extra_data['grade']
            if grade_value and str(grade_value).strip() not in ['', 'N/A', 'None', 'nan', 'NaN']:
                all_fields.append(('GRADE', str(grade_value)))
        
        # Add COMMENT - check both comment field and extra_data
        comment_value = None
        if student.comment:
            comment_value = student.comment
        elif student.extra_data and 'comment' in student.extra_data:
            comment_value = student.extra_data['comment']
        
        if comment_value and str(comment_value).strip() not in ['', 'N/A', 'None', 'nan', 'NaN']:
            all_fields.append(('COMMENT', str(comment_value)))
            print(f"\n[OK] COMMENT WILL BE DISPLAYED: {comment_value}")
        else:
            print(f"\n[NO] NO COMMENT TO DISPLAY")
        
        print("\n" + "=" * 80)
        print(f"Total fields to display: {len(all_fields)}")
        print("=" * 80)
        
        # Show table structure
        print("\nEmail table columns:")
        for key, value in all_fields:
            print(f"  - {key}: {value}")

if __name__ == '__main__':
    test_comment_display()
