"""
Generate a test email HTML to preview the comment display
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import Student
from email_service import send_email_to_student
from datetime import datetime
import pytz

BANGKOK_TZ = pytz.timezone('Asia/Bangkok')

def generate_test_email():
    """Generate test email HTML with comment"""
    
    app = create_app()
    
    with app.app_context():
        # Get a student with a comment
        student = Student.query.filter_by(name='Seyha Ny').first()
        
        if not student:
            print("Student not found!")
            return
        
        print(f"Generating test email for: {student.name}")
        print(f"Score: {student.score}")
        print(f"Comment: {student.comment}")
        print("=" * 80)
        
        # Generate the HTML manually (same logic as email_service.py)
        score_color = "#f39c12"
        try:
            score_value = float(student.score) if student.score else 0
            if score_value >= 80:
                score_color = "#27ae60"
            elif score_value >= 60:
                score_color = "#f39c12"
            else:
                score_color = "#e74c3c"
        except:
            score_color = "#f39c12"
        
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
        
        # Build table
        all_fields = []
        
        # Add FIRST NAME and LAST NAME
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
        
        # Add COMMENT
        comment_value = None
        if student.comment:
            comment_value = student.comment
        elif student.extra_data and 'comment' in student.extra_data:
            comment_value = student.extra_data['comment']
        
        if comment_value and str(comment_value).strip() not in ['', 'N/A', 'None', 'nan', 'NaN']:
            all_fields.append(('COMMENT', str(comment_value)))
        
        # Build headers
        table_html = ""
        for key, value in all_fields:
            label = key.replace('_', ' ').replace('-', ' ').upper()
            table_html += f'''
                                    <th style="padding: 14px 12px; text-align: left; color: white; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; border-right: 1px solid rgba(255,255,255,0.2); white-space: nowrap;">{label}</th>'''
        
        table_html += '''
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="background-color: #f8f9fa;">'''
        
        # Build data cells
        for key, value in all_fields:
            is_highlight = key.lower() in ['total', 'grade', 'score']
            
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
        
        # Add encouragement
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
        
        # Save to file
        output_file = "test_email_with_comment_preview.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_body)
        
        print(f"\n[OK] Test email HTML generated: {output_file}")
        print(f"[OK] Comment '{comment_value}' is included in the table")
        print("\nOpen the HTML file in your browser to see the preview!")

if __name__ == '__main__':
    generate_test_email()
