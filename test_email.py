"""
Simple Email Test Script
Run this to test if your Gmail credentials work for sending emails
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_sending():
    """Test email sending with Gmail"""
    
    print("=" * 60)
    print("Gmail Email Test Script")
    print("=" * 60)
    
    # Get credentials from user
    sender_email = input("\nEnter your Gmail address: ").strip()
    app_password = input("Enter your Gmail App Password (16 characters): ").strip()
    recipient_email = input("Enter test recipient email (can be your own): ").strip()
    
    print("\n" + "=" * 60)
    print("Testing email configuration...")
    print("=" * 60)
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Test Email from Student Results System"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # Email body
        text = """
        This is a test email from your Student Results System.
        
        If you received this, your email configuration is working correctly!
        
        You can now send student results using this email address.
        """
        
        html = """
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #2563eb;">✅ Email Test Successful!</h2>
            <p>This is a test email from your <strong>Student Results System</strong>.</p>
            <p>If you received this, your email configuration is working correctly!</p>
            <p style="color: #16a34a; font-weight: bold;">
              ✓ You can now send student results using this email address.
            </p>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #e5e7eb;">
            <p style="color: #6b7280; font-size: 12px;">
              Sent from Student Results System<br>
              Gmail SMTP Server
            </p>
          </body>
        </html>
        """
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Connect to Gmail SMTP server
        print("\n1. Connecting to Gmail SMTP server (smtp.gmail.com:587)...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        
        print("2. Starting TLS encryption...")
        server.starttls()
        
        print("3. Logging in with your credentials...")
        server.login(sender_email, app_password)
        
        print("4. Sending test email...")
        server.sendmail(sender_email, recipient_email, message.as_string())
        
        print("5. Closing connection...")
        server.quit()
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Email sent successfully!")
        print("=" * 60)
        print(f"\nFrom: {sender_email}")
        print(f"To: {recipient_email}")
        print(f"Subject: Test Email from Student Results System")
        print("\nCheck your inbox (or spam folder) for the test email.")
        print("\n✅ Your email configuration is working!")
        print("You can now use these credentials in the app to send student results.")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("\n" + "=" * 60)
        print("❌ AUTHENTICATION FAILED")
        print("=" * 60)
        print("\nError:", str(e))
        print("\n🔧 How to fix:")
        print("1. Make sure you're using a Gmail App Password, NOT your regular password")
        print("2. Generate App Password here: https://myaccount.google.com/apppasswords")
        print("3. Enable 2-Step Verification first")
        print("4. Copy the 16-character password exactly (no spaces)")
        return False
        
    except smtplib.SMTPException as e:
        print("\n" + "=" * 60)
        print("❌ SMTP ERROR")
        print("=" * 60)
        print("\nError:", str(e))
        print("\n🔧 Possible issues:")
        print("1. Check your internet connection")
        print("2. Gmail SMTP might be blocked by firewall")
        print("3. Try again in a few minutes")
        return False
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print("\nError:", str(e))
        print("\n🔧 Please check:")
        print("1. Email addresses are valid")
        print("2. App Password is correct")
        print("3. Internet connection is working")
        return False

if __name__ == "__main__":
    print("\n🔐 Gmail App Password Required!")
    print("Generate one here: https://myaccount.google.com/apppasswords")
    print("(You need 2-Step Verification enabled first)\n")
    
    test_email_sending()
    
    input("\nPress Enter to exit...")
