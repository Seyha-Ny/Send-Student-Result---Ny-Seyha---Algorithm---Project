"""
Fix database by adding comment column to all database files
"""
import sqlite3
import os

def add_comment_column(db_path):
    """Add comment column to a specific database file"""
    if not os.path.exists(db_path):
        print(f"[SKIP] Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if comment column exists
        cursor.execute("PRAGMA table_info(students)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'comment' not in columns:
            print(f"[UPDATING] Adding 'comment' column to: {db_path}")
            cursor.execute("ALTER TABLE students ADD COLUMN comment TEXT")
            conn.commit()
            print(f"[SUCCESS] Added 'comment' column to: {db_path}")
            return True
        else:
            print(f"[INFO] 'comment' column already exists in: {db_path}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error updating {db_path}: {str(e)}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("DATABASE MIGRATION: Adding 'comment' column")
    print("=" * 60)
    
    # List of possible database locations
    db_locations = [
        r'instance\student_results.db',
        r'send_students_result_nyseyha\instance\student_results.db',
        r'student_results.db'
    ]
    
    updated_count = 0
    for db_path in db_locations:
        full_path = os.path.join(os.path.dirname(__file__), db_path)
        if add_comment_column(full_path):
            updated_count += 1
    
    print("=" * 60)
    print(f"Migration complete! Updated {updated_count} database(s)")
    print("=" * 60)
    print("\nPlease RESTART your application for changes to take effect!")
