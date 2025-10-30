# Send Student Result System

A web-based application that allows teachers and administrators to send student scores automatically via email with just one click. This system helps reduce time spent manually composing and sending emails, improves communication efficiency, and ensures that every student receives their result securely and instantly.

## 🎯 Features

### 1. **File Upload & Processing**
- Upload student result files in CSV or Excel format
- Automatic data validation and parsing
- Support for required columns: name, email, score
- Optional columns: subject, batch

### 2. **Data Preview**
- View all uploaded student data in a responsive table
- Search and filter functionality
- Real-time statistics (total students, valid emails, average score)
- Select individual or all students for sending

### 3. **Bulk Email Sending**
- Send personalized emails to all students with one click
- Professional HTML email templates
- Automatic error handling and retry logic
- Real-time sending status updates

### 4. **Email Logging & Tracking**
- Track email delivery status (sent, failed, pending)
- View detailed error messages for failed emails
- Export logs as CSV for record keeping
- Auto-refresh logs every 30 seconds

### 5. **Responsive Design**
- Clean and intuitive user interface
- Mobile-friendly design using Tailwind CSS
- Real-time notifications and feedback
- Smooth animations and transitions

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Tailwind CSS
- **Database**: SQLite (default) or MySQL
- **Email**: Flask-Mail with SMTP support
- **Data Processing**: Pandas, OpenPyXL
- **Server**: Werkzeug

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)
- SMTP email account (Gmail, Outlook, SendGrid, etc.)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd send_students_result_nyseyha
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your email configuration:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///student_results.db

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=noreply@studentresults.com
```

### 5. Email Configuration Guide

#### **Gmail Setup**
1. Enable 2-Factor Authentication on your Google Account
2. Go to https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer" (or your device)
4. Generate an App Password
5. Use the generated password in `.env` file

#### **Outlook/Office 365**
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USERNAME=your_email@outlook.com
MAIL_PASSWORD=your_password
```

#### **SendGrid**
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your_sendgrid_api_key
```

### 6. Initialize Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 7. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 📖 Usage Guide

### Step 1: Upload Student Data

1. Navigate to the home page (Upload section)
2. Click on the upload area or drag and drop a CSV/Excel file
3. Ensure your file has the required columns: `name`, `email`, `score`
4. Click "Upload File" button
5. The system will validate and save the data

### Step 2: Preview Data

1. After upload, you'll be redirected to the Preview page
2. Review the student list and statistics
3. Use the search bar to find specific students
4. Select individual students or click "Select All"

### Step 3: Send Results

1. Click "Send All Results" or "Send Selected"
2. Confirm the action in the popup dialog
3. The system will send personalized emails to all selected students
4. Monitor the sending progress

### Step 4: Check Logs

1. Navigate to the Logs page
2. View all email delivery statuses
3. Filter by status (Sent, Failed, Pending)
4. Search for specific students
5. Export logs as CSV for record keeping

## 📁 File Format

### CSV Format Example

```csv
name,email,score,subject,batch
John Doe,john@example.com,85.5,Mathematics,2024-A
Jane Smith,jane@example.com,92.0,Physics,2024-B
```

### Excel Format
- Same columns as CSV
- Supported formats: .xlsx, .xls

## 🗂️ Project Structure

```
send_students_result_nyseyha/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── routes.py              # API routes and endpoints
├── email_service.py       # Email sending logic
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── sample_data.csv        # Sample student data
├── README.md              # This file
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Upload page
│   ├── preview.html       # Preview page
│   └── logs.html          # Logs page
└── uploads/               # Uploaded files directory
```

## 🔌 API Endpoints

### File Upload
- **POST** `/api/upload` - Upload and process student file
- **POST** `/api/save-students` - Save students to database

### Student Management
- **GET** `/api/students` - Get all students
- **POST** `/api/send-results` - Send results to students

### Email Logs
- **GET** `/api/email-logs` - Get all email logs
- **GET** `/api/email-logs/export` - Export logs as CSV

### Health Check
- **GET** `/api/health` - Health check endpoint

## 🔒 Security Features

- File upload validation (only CSV and Excel files)
- Email format validation
- SQL injection prevention (SQLAlchemy ORM)
- CSRF protection ready
- Secure password handling with environment variables
- Database encryption support

## 🐛 Troubleshooting

### Issue: "SMTP Authentication Failed"
- **Solution**: Check your email credentials in `.env` file
- For Gmail, ensure you're using an App Password, not your regular password
- Verify 2-Factor Authentication is enabled

### Issue: "File Upload Failed"
- **Solution**: Ensure file is in CSV or Excel format
- Check that required columns (name, email, score) are present
- Verify file size is less than 16MB

### Issue: "Emails Not Sending"
- **Solution**: Check SMTP configuration in `.env`
- Verify email account has SMTP access enabled
- Check firewall/antivirus settings
- Review error messages in the Logs page

### Issue: "Database Error"
- **Solution**: Delete `student_results.db` file and reinitialize
- Run: `python app.py` to recreate the database

## 📊 Database Schema

### Students Table
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    score FLOAT NOT NULL,
    subject VARCHAR(120),
    batch VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Email Logs Table
```sql
CREATE TABLE email_logs (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    sent_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
```

## 🎨 Customization

### Change Email Template
Edit the `send_email_to_student()` function in `email_service.py` to customize the email HTML template.

### Modify UI Colors
Edit the Tailwind CSS classes in template files to change colors and styling.

### Add Custom Fields
1. Update the Student model in `models.py`
2. Update the CSV parsing in `routes.py`
3. Update the HTML templates

## 📝 License

This project is open source and available for educational and commercial use.

## 👨‍💻 Support

For issues, questions, or suggestions, please refer to the troubleshooting section or contact the development team.

## 🎓 Educational Value

This project demonstrates:
- Flask web framework fundamentals
- RESTful API design
- Database modeling with SQLAlchemy
- Email integration with SMTP
- Frontend-backend integration
- File upload handling
- Data validation and error handling
- Responsive web design with Tailwind CSS

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready

