"""
Database models for Student Results System
"""
from datetime import datetime
from extensions import db

class Student(db.Model):
    """Student model to store student information and results"""
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50))
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    score = db.Column(db.Float, nullable=False)
    subject = db.Column(db.String(120))
    batch = db.Column(db.String(50))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'score': self.score,
            'subject': self.subject,
            'batch': self.batch,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class EmailLog(db.Model):
    """Email log model to track email sending status"""
    __tablename__ = 'email_logs'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    error_message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert email log object to dictionary"""
        student = Student.query.get(self.student_id)
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': student.name if student else 'Unknown',
            'student_email': student.email if student else 'Unknown',
            'status': self.status,
            'error_message': self.error_message,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

