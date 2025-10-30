"""
Migration script to sync existing comments to extra_data field
This ensures comments appear in email results
"""
from app import app, db
from models import Student

def sync_comments_to_extra_data():
    """Sync all existing comments to extra_data field"""
    with app.app_context():
        students = Student.query.all()
        updated_count = 0
        
        for student in students:
            if student.comment:
                # Initialize extra_data if None
                if student.extra_data is None:
                    student.extra_data = {}
                
                # Add comment to extra_data
                student.extra_data['comment'] = student.comment
                updated_count += 1
                print(f"Synced comment for {student.name} ({student.email})")
        
        db.session.commit()
        print(f"\nSuccessfully synced {updated_count} comments to extra_data")
        print(f"Total students: {len(students)}")

if __name__ == '__main__':
    print("Starting comment sync to extra_data...")
    sync_comments_to_extra_data()
    print("Done!")
