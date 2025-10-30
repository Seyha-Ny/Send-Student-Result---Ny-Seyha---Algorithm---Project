"""
Email service for sending student results
"""
from flask_mail import Message
from flask import current_app, render_template_string
from extensions import mail, db
from models import EmailLog
from datetime import datetime

def send_email_to_student(student):
    """
    Send email to a single student with their result
    
    Args:
        student: Student object
    
    Returns:
        dict: Status of email sending
    """
    try:
        # Create email log entry
        email_log = EmailLog(
            student_id=student.id,
            status='pending'
        )
        db.session.add(email_log)
        db.session.commit()
        
        # Prepare email content
        subject = f"Your Academic Result - {student.subject or 'Score'}"
        
        # Email body template
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">Hello {student.name},</h2>
                    
                    <p>We are pleased to share your academic result with you.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #2c3e50; margin-top: 0;">Result Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px; font-weight: bold;">Student ID:</td>
                                <td style="padding: 10px;">{student.student_id or 'N/A'}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px; font-weight: bold;">Subject:</td>
                                <td style="padding: 10px;">{student.subject or 'N/A'}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px; font-weight: bold;">Score:</td>
                                <td style="padding: 10px; font-size: 18px; color: #27ae60; font-weight: bold;">{student.score}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #ddd;">
                                <td style="padding: 10px; font-weight: bold;">Batch:</td>
                                <td style="padding: 10px;">{student.batch or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; font-weight: bold;">Comment:</td>
                                <td style="padding: 10px;">{student.comment or 'No comment'}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p>If you have any questions regarding your result, please contact your instructor.</p>
                    
                    <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px;">
                        This is an automated email. Please do not reply to this message.
                    </p>
                </div>
            </body>
        </html>
        """
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[student.email],
            html=html_body
        )
        
        # Send email
        mail.send(msg)
        
        # Update email log
        email_log.status = 'sent'
        email_log.sent_at = datetime.utcnow()
        db.session.commit()
        
        return {
            'student_id': student.id,
            'student_name': student.name,
            'email': student.email,
            'status': 'sent',
            'message': 'Email sent successfully'
        }
    
    except Exception as e:
        # Update email log with error
        email_log = EmailLog.query.filter_by(student_id=student.id).order_by(EmailLog.created_at.desc()).first()
        if email_log:
            email_log.status = 'failed'
            email_log.error_message = str(e)
            db.session.commit()
        
        return {
            'student_id': student.id,
            'student_name': student.name,
            'email': student.email,
            'status': 'failed',
            'message': f'Error sending email: {str(e)}'
        }

def send_student_results(students):
    """
    Send results to multiple students
    
    Args:
        students: List of Student objects
    
    Returns:
        dict: Summary of sending results
    """
    results = {
        'total': len(students),
        'sent': 0,
        'failed': 0,
        'details': []
    }
    
    for student in students:
        result = send_email_to_student(student)
        results['details'].append(result)
        
        if result['status'] == 'sent':
            results['sent'] += 1
        else:
            results['failed'] += 1
    
    return results

