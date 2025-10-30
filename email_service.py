import os
from datetime import datetime
from typing import List
import pytz

from flask_mail import Message
from flask import current_app
from extensions import mail, db
from models import EmailLog, get_bangkok_time

# Define Bangkok timezone
BANGKOK_TZ = pytz.timezone('Asia/Bangkok')

def get_auto_comment(score):
    """
    Generate automatic comment based on score
    
    Args:
        score: Student's score (numeric)
    
    Returns:
        str: Auto-generated comment
    """
    try:
        score_value = float(score) if score else 0
        
        if score_value >= 90:
            return "Excellent work! Outstanding performance!"
        elif score_value >= 85:
            return "Great job! Keep up the excellent work!"
        elif score_value >= 80:
            return "Very good! You're doing great!"
        elif score_value >= 75:
            return "Good work! Keep pushing forward!"
        elif score_value >= 70:
            return "Nice effort! Keep improving!"
        elif score_value >= 65:
            return "Good try! You can do better!"
        elif score_value >= 60:
            return "Keep working! You're making progress!"
        else:
            return "Try more! Don't give up!"
    except:
        return "Keep learning and growing!"

def send_email_to_student(student, owner_email=None):
    """
    Send email to a single student with their result
    
    Args:
        student: Student object
        owner_email (str, optional): If provided, a copy of the email will be sent to this address.
    
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
        subject = f"📄 Your Academic Result - {student.subject or 'Assessment'}"
        
        # Determine score color based on performance (if score exists and is numeric)
        score_color = "#f39c12"  # Default orange
        try:
            score_value = float(student.score) if student.score else 0
            if score_value >= 80:
                score_color = "#27ae60"  # Green for high scores
            elif score_value >= 60:
                score_color = "#f39c12"  # Orange for medium scores
            else:
                score_color = "#e74c3c"  # Red for low scores
        except:
            score_color = "#f39c12"  # Default if score is not numeric
        
        # Email body template - Clean minimalist design matching the uploaded image
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your Academic Result</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f5f7fa;">
            <div style="max-width: 600px; margin: 40px auto; padding: 20px;">
                
                <!-- Header with Title -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px 12px 0 0; padding: 30px; text-align: center;">
                    <h1 style="margin: 0; color: white; font-size: 24px; font-weight: 600;">📊 Academic Results</h1>
                    <p style="margin: 8px 0 0 0; color: rgba(255,255,255,0.9); font-size: 14px;">Your performance summary is ready</p>
                </div>
                
                <!-- Main Card -->
                <div style="background: linear-gradient(135deg, #e8eaf6 0%, #c5cae9 100%); border-radius: 0 0 16px 16px; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
                    
                    <!-- Personalized Greeting -->
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h2 style="margin: 0; font-size: 22px; color: #202124; font-weight: 500;">
                            Hello {student.name.upper()}! 👋
                        </h2>
                        <p style="margin: 8px 0 0 0; font-size: 14px; color: #5f6368;">
                            We're excited to share your academic results with you. Here's how you performed!
                        </p>
                    </div>
                    
                    <!-- Score Circle -->
                    <div style="text-align: center; margin-bottom: 30px;">
                        <div style="background-color: {score_color}; color: white; font-size: 52px; font-weight: bold; border-radius: 50%; width: 160px; height: 160px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.15); display: table;">
                            <span style="display: table-cell; vertical-align: middle; text-align: center;">{student.score}</span>
                        </div>
                        <p style="margin: 20px 0 0 0; font-size: 20px; color: #5f6368; font-weight: 500;">
                            Your Score
                        </p>
                    </div>
                    
                    <!-- Results Table -->
                    <div style="background-color: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); overflow-x: auto;">
                        <table style="width: 100%; border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;">
                            <thead>
                                <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">"""
        
        # Build table header and rows
        table_html = ""
        
        # Define the desired order: FIRST NAME, LAST NAME, SUBJECTS (no scores), Total, Grade
        all_fields = []
        has_comment = False
        
        # Add FIRST NAME and LAST NAME first
        if student.extra_data and 'first_name' in student.extra_data:
            all_fields.append(('FIRST NAME', student.extra_data['first_name']))
        if student.extra_data and 'last_name' in student.extra_data:
            all_fields.append(('LAST NAME', student.extra_data['last_name']))
        
        # Add SUBJECTS with their scores - subject name as header, score as value
        if student.extra_data:
            # Collect subject-score pairs
            subject_scores = {}
            for key in sorted(student.extra_data.keys()):
                if key.startswith('subject_'):
                    # Extract the number from subject_1, subject_2, etc.
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
            
            # Add subjects in order - subject name as column header, score as value
            for num in sorted(subject_scores.keys(), key=lambda x: int(x)):
                subject_data = subject_scores[num]
                # Use subject name as the header (e.g., "hg", "gh")
                all_fields.append((subject_data['name'].upper(), subject_data['score']))
        
        # Add TOTAL (the score)
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
            has_comment = True
            all_fields.append(('COMMENT', str(comment_value)))
        
        # Build table headers
        for i, (key, value) in enumerate(all_fields):
            label = key.replace('_', ' ').replace('-', ' ').upper()
            table_html += f'''
                                    <th style="padding: 14px 12px; text-align: left; color: white; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; border-right: 1px solid rgba(255,255,255,0.2); white-space: nowrap;">{label}</th>'''
        
        table_html += '''
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="background-color: #f8f9fa;">'''
        
        # Build table data cells
        for i, (key, value) in enumerate(all_fields):
            # Determine if this is a highlighted field
            is_highlight = key.lower() in ['total', 'grade', 'score']
            
            # Style based on field type
            if is_highlight:
                cell_style = "padding: 14px 12px; font-size: 15px; font-weight: 700; color: #202124; border-right: 1px solid #dee2e6; border-bottom: 2px solid #667eea; background-color: #fff3cd;"
            else:
                cell_style = "padding: 14px 12px; font-size: 14px; font-weight: 500; color: #495057; border-right: 1px solid #dee2e6;"
            
            table_html += f'''
                                    <td style="{cell_style}">{value}</td>'''
        
        table_html += '''
                                </tr>
                            </tbody>
                        </table>
                    </div>'''
        
        html_body += table_html
        
        # Add encouragement message based on score
        try:
            score_value = float(student.score) if student.score else 0
            if score_value >= 90:
                encouragement = "🎉 Excellent work! Keep up the great performance!"
                msg_color = "#27ae60"
            elif score_value >= 80:
                encouragement = "👏 Great job! You're doing very well!"
                msg_color = "#27ae60"
            elif score_value >= 70:
                encouragement = "👍 Good work! Keep pushing forward!"
                msg_color = "#f39c12"
            elif score_value >= 60:
                encouragement = "💪 Keep working hard! You're making progress!"
                msg_color = "#f39c12"
            else:
                encouragement = "📚 Don't give up! Every effort counts towards improvement!"
                msg_color = "#e74c3c"
        except:
            encouragement = "📚 Keep learning and growing!"
            msg_color = "#667eea"
        
        html_body += f"""
                        
                    </div>
                    
                    <!-- Encouragement Message -->
                    <div style="background-color: {msg_color}; color: white; border-radius: 8px; padding: 16px 24px; margin-top: 24px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        <p style="margin: 0; font-size: 15px; font-weight: 500; line-height: 1.5;">
                            {encouragement}
                        </p>
                    </div>
                    
                </div>
                
                <!-- Footer -->
                <div style="text-align: center; margin-top: 30px; padding: 20px;">
                    <p style="color: #80868b; font-size: 13px; margin: 0; line-height: 1.6;">
                        This is an automated email from the Student Results System.<br>
                        Please do not reply to this message.
                    </p>
                    <p style="color: #9aa0a6; font-size: 12px; margin: 12px 0 0 0;">
                        Generated on {datetime.now(BANGKOK_TZ).strftime('%B %d, %Y at %I:%M %p')} (Bangkok Time)
                    </p>
                </div>
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
        
        # If owner_email is provided, add it as a BCC recipient
        if owner_email:
            msg.bcc = [owner_email]

        # Send email
        mail.send(msg)
        
        # Update email log
        email_log.status = 'sent'
        email_log.sent_at = get_bangkok_time()
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

def send_student_results(students: List, owner_email: str = None):
    """
    Send results to multiple students
    
    Args:
        students: List of Student objects
        owner_email (str, optional): If provided, a copy of each email will be sent to this address.
    
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
        result = send_email_to_student(student, owner_email)
        results['details'].append(result)
        
        if result['status'] == 'sent':
            results['sent'] += 1
        else:
            results['failed'] += 1
    
    return results
