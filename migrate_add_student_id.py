"""
Migration script to add student_id column to students table
Run this script to update the database schema
"""
import os
from app import app, db
from models import Student

def migrate():
    """Add student_id column to students table"""
    with app.app_context():
        try:
            # Check if column already exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('students')]
            
            if 'student_id' in columns:
                print("[OK] student_id column already exists")
                return
            
            # Add the column using raw SQL
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE students ADD COLUMN student_id VARCHAR(50)'))
                conn.commit()
            
            print("[OK] Successfully added student_id column to students table")
            
        except Exception as e:
            print(f"[ERROR] Error during migration: {str(e)}")
            raise

if __name__ == '__main__':
    print("Starting database migration...")
    migrate()
    print("Migration completed!")
