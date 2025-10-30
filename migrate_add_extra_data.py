"""
Migration script to add extra_data column to students table
"""
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("PRAGMA table_info(students)"))
            columns = [row[1] for row in result]
            
            if 'extra_data' not in columns:
                print("Adding extra_data column to students table...")
                db.session.execute(text("ALTER TABLE students ADD COLUMN extra_data JSON"))
                db.session.commit()
                print("SUCCESS: Successfully added extra_data column!")
            else:
                print("INFO: extra_data column already exists!")
                
        except Exception as e:
            print(f"ERROR: Error during migration: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    migrate()
