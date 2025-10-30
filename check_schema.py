"""Check database schema"""
from app import app, db
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    columns = inspector.get_columns('students')
    print('Columns in students table:')
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")
