"""
Database migration script to add comment column to students table
Run this script once to update your existing database
"""
import sys
import io
from app import app, db
from sqlalchemy import text

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def migrate():
    with app.app_context():
        try:
            # Check if comment column already exists
            result = db.session.execute(text("PRAGMA table_info(students)"))
            columns = [row[1] for row in result]
            
            if 'comment' not in columns:
                print("Adding 'comment' column to students table...")
                db.session.execute(text("ALTER TABLE students ADD COLUMN comment TEXT"))
                db.session.commit()
                print("[SUCCESS] Successfully added 'comment' column")
            else:
                print("[INFO] 'comment' column already exists")
                
        except Exception as e:
            print(f"[ERROR] Error during migration: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    print("Starting database migration...")
    migrate()
    print("Migration complete!")
