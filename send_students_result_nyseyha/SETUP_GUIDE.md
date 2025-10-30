# Setup Guide - Send Student Result System

This guide provides step-by-step instructions to set up and run the Send Student Result System on your computer.

## Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- pip (Python package manager)
- A text editor or IDE (VS Code, PyCharm, etc.)
- An email account with SMTP access (Gmail, Outlook, SendGrid, etc.)

## Step-by-Step Installation

### 1. Extract Project Files

Extract the project files to your desired location:
```
C:\Users\YourUsername\Desktop\send_students_result_nyseyha
```

### 2. Open Command Prompt/Terminal

Navigate to the project directory:
```bash
cd C:\Users\YourUsername\Desktop\send_students_result_nyseyha
```

### 3. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- Flask
- Flask-Mail
- Flask-SQLAlchemy
- Pandas
- python-dotenv
- And others

### 5. Configure Email Settings

#### Option A: Gmail (Recommended for Testing)

1. **Enable 2-Factor Authentication:**
   - Go to https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process

2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - Copy the 16-character password

3. **Create .env file:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add:
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   MAIL_DEFAULT_SENDER=your_email@gmail.com
   ```

#### Option B: Outlook/Office 365

```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@outlook.com
MAIL_PASSWORD=your_password
MAIL_DEFAULT_SENDER=your_email@outlook.com
```

#### Option C: SendGrid

```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.your_sendgrid_api_key
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

### 6. Initialize Database

Run Python and create the database:

```bash
python
```

Then in the Python shell:
```python
from app import app, db
with app.app_context():
    db.create_all()
print("Database created successfully!")
exit()
```

### 7. Run the Application

```bash
python app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 8. Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

## First Time Usage

### Test with Sample Data

1. **Download or use the sample CSV:**
   - The project includes `sample_data.csv` with test data
   - Or create your own CSV file with columns: name, email, score, subject, batch

2. **Upload the file:**
   - Click on the upload area
   - Select your CSV file
   - Click "Upload File"

3. **Preview the data:**
   - Review the student list
   - Check statistics
   - Verify email addresses

4. **Send test emails:**
   - Click "Send All Results"
   - Confirm the action
   - Monitor the sending progress

5. **Check logs:**
   - Go to the Logs page
   - View delivery status
   - Export logs if needed

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

### Problem: "SMTP Authentication Failed"

**Solution:**
1. Verify email and password in `.env` file
2. For Gmail, ensure you're using App Password (not regular password)
3. Check that 2-Factor Authentication is enabled
4. Try a different email provider (Outlook, SendGrid)

### Problem: "Port 5000 already in use"

**Solution:**
```bash
# Change the port in app.py
# Change: app.run(debug=True, host='0.0.0.0', port=5000)
# To: app.run(debug=True, host='0.0.0.0', port=5001)
```

### Problem: "Database locked" error

**Solution:**
1. Close the application
2. Delete `student_results.db` file
3. Run `python app.py` again to recreate the database

### Problem: "File upload failed"

**Solution:**
1. Ensure file is CSV or Excel format
2. Check that required columns exist: name, email, score
3. Verify file size is less than 16MB
4. Check for special characters in file names

## File Format Requirements

### CSV File Format

Create a CSV file with the following columns:

```
name,email,score,subject,batch
John Doe,john@example.com,85.5,Mathematics,2024-A
Jane Smith,jane@example.com,92.0,Physics,2024-B
```

**Required columns:**
- `name` - Student's full name
- `email` - Student's email address
- `score` - Numeric score (can be decimal)

**Optional columns:**
- `subject` - Subject or course name
- `batch` - Batch or class identifier

### Excel File Format

Same structure as CSV, but in .xlsx or .xls format.

## Project Structure

```
send_students_result_nyseyha/
├── app.py                 # Main application file
├── models.py              # Database models
├── routes.py              # API endpoints
├── email_service.py       # Email sending logic
├── utils.py               # Helper functions
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
├── sample_data.csv        # Sample data
├── README.md              # Full documentation
├── SETUP_GUIDE.md         # This file
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Upload page
│   ├── preview.html       # Preview page
│   └── logs.html          # Logs page
└── uploads/               # Uploaded files
```

## Next Steps

1. **Customize Email Template:**
   - Edit `email_service.py`
   - Modify the HTML email template

2. **Add More Features:**
   - Add user authentication
   - Implement email scheduling
   - Add email templates selection

3. **Deploy to Production:**
   - Use Gunicorn or uWSGI
   - Set up with Nginx or Apache
   - Use a production database (PostgreSQL, MySQL)

## Support & Help

- Check the README.md for detailed documentation
- Review error messages in the Logs page
- Check the browser console for JavaScript errors
- Verify email configuration settings

## Security Notes

- Never commit `.env` file to version control
- Use strong, unique passwords
- Keep dependencies updated
- Use HTTPS in production
- Validate all user inputs

---

**Happy emailing! 📧**

