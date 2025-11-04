# 📄 Student Results Email System

A modern web application that automatically sends student results via email using Excel files and Gmail. Perfect for teachers and administrators who need to quickly distribute academic results to students.

## ✨ Key Features

### 📊 **Smart File Upload (.xlsx, .csv)**
- Drag & drop Excel/CSV file upload
- **Intelligent column detection** - automatically handles any file structure
- **Only email column required** - all other fields are optional
- **Dynamic extra fields** - automatically stores and displays any additional columns
- Handles files with/without headers
- Auto-maps common column variations (firstname/lastname → name, total → score, etc.)
- Real-time data validation

### 📧 **Gmail Integration** 
- Easy Gmail configuration with App Passwords
- Test email settings before sending
- Secure SMTP connection via Gmail
- **Sender uses their own Gmail credentials** for sending
- Optional BCC to owner email for monitoring

### 🚀 **One-Click Send**
- **"Send Results Now"** button for instant delivery
- Send to all students or selected students
- Real-time progress tracking
- Automatic error handling and retry logic

### 📈 **Beautiful Email Templates**
- Modern gradient design with responsive layout
- **Dynamic table generation** - displays all student data fields
- Color-coded scores (Green: 80+, Orange: 60-79, Red: <60)
- Personalized encouragement messages based on performance
- Displays subjects with scores, grades, comments, and custom fields
- Mobile-friendly email layout

### 💬 **Comment System**
- Add/edit comments for individual students
- Comments automatically included in emails
- Inline editing in preview table

### 🔗 **Result Sharing**
- Generate secure shareable links for student results
- Set expiration dates for shared links
- Track view counts and access history
- Deactivate links anytime

### 📋 **Comprehensive Logging**
- Track email delivery status (sent, failed, pending)
- View detailed error messages
- Export logs as CSV
- Real-time status updates
- Bangkok timezone support

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

### 4. Configure Environment Variables (Optional)

Create a `.env` file in the project root directory for advanced configuration:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///student_results.db

# Email Configuration (Optional - can be set via UI)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
MAIL_OWNER_EMAIL=admin@example.com  # Optional: Receive BCC of all emails
```

**Note:** Email credentials can be entered directly in the web interface, so `.env` configuration is optional.

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

### 6. Run the Application

**Option A: Quick Start (Recommended)**

```bash
# Windows
quickstart.bat

# macOS/Linux
./quickstart.sh
```

**Option B: Manual Start**

```bash
python app.py
```

The database will be created automatically on first run.

The application will be available at: **http://localhost:5000**

## 📖 Usage Guide

### Step 1: Upload Student Data (.xlsx or .csv file)

1. Navigate to the home page
2. In the **Upload Student Results** section:
   - Drag & drop your Excel/CSV file or click to browse
   - **Only required column: `email`** (all other fields are optional)
   - The system automatically handles any additional columns
   - Supports files with or without headers
3. Click **"Upload File"** button
4. Preview the uploaded data in the table
5. Click **"Save to Database"** to store the data

**Supported File Formats:**
- Any column structure (only email is required)
- Automatically detects: name, score, student_id, subject, batch, comment
- All extra columns are preserved and displayed in emails
- Auto-maps variations: firstname+lastname→name, total→score, class→batch

### Step 2: Review and Edit (Optional)

1. View all students in the preview table
2. Click on any student row to edit their information
3. Add or modify comments for individual students
4. Comments will be included in the email

### Step 3: Configure Gmail and Send

1. In the **Gmail Configuration** section:
   - Enter your Gmail address (e.g., `youremail@gmail.com`)
   - Enter your Gmail App Password (generate at https://myaccount.google.com/apppasswords)
2. Click **"Test Email Configuration"** to verify settings
3. ✅ You should see "Email configuration is valid!" message
4. Click the big **"Send Results Now"** button
5. Confirm the action in the popup dialog
6. ✅ All students receive personalized emails from your Gmail!

### Step 4: Monitor Results

1. Click **"View Logs"** in the navigation to see delivery status
2. Check sent/failed email counts
3. Export logs as CSV for record keeping
4. Review any error messages for failed deliveries

### Step 5: Share Results (Optional)

1. Select students to share
2. Click **"Share Results"** button
3. Enter recipient email and expiration date
4. Generate secure shareable link
5. Send link to authorized viewers

## 📁 File Format

### Minimal Format (Only Email Required)

```csv
email
john@example.com
jane@example.com
```

### Standard Format Example

```csv
name,email,score,subject,batch
John Doe,john@example.com,85.5,Mathematics,2024-A
Jane Smith,jane@example.com,92.0,Physics,2024-B
```

### Extended Format with Custom Fields

```csv
first_name,last_name,email,subject_1,score_1,subject_2,score_2,total,grade,comment
John,Doe,john@example.com,Math,85,Science,90,175,A,Excellent work!
Jane,Smith,jane@example.com,Math,92,Science,88,180,A+,Outstanding!
```

**Key Points:**
- **Only `email` column is required**
- All other columns are optional and flexible
- System automatically handles any additional columns
- Extra columns are stored and displayed in emails
- Supported formats: .xlsx, .xls, .csv
- Files can have headers or no headers (auto-detected)

## 🗂️ Project Structure

```
send_students_result_nyseyha/
├── app.py                 # Main Flask application with app factory
├── models.py              # Database models (Student, EmailLog, SharedResult)
├── routes.py              # API routes and endpoints
├── email_service.py       # Email sending logic with dynamic templates
├── extensions.py          # Flask extensions (SQLAlchemy, Flask-Mail)
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── sample_students.csv    # Sample student data
├── quickstart.bat         # Windows quick start script
├── quickstart.sh          # Unix/Linux quick start script
├── README.md              # This file
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Upload and send page
│   ├── preview.html       # Preview and edit students
│   ├── logs.html          # Email logs page
│   ├── help.html          # Help and FAQ page
│   └── shared_results.html # Shared results view
├── uploads/               # Uploaded files directory
└── instance/              # SQLite database location
    └── student_results.db # SQLite database file
```

## 🔌 API Endpoints

### File Upload & Processing
- **POST** `/api/upload` - Upload and process student file (CSV/Excel)
- **POST** `/api/map-columns` - Manual column mapping for files with missing fields
- **POST** `/api/save-students` - Save students to database
- **GET** `/api/download-sample` - Download sample CSV template

### Student Management
- **GET** `/api/students` - Get all students
- **PUT** `/api/students/<id>` - Update student information
- **PUT** `/api/students/<id>/comment` - Update student comment
- **DELETE** `/api/clear-students` - Clear all students and logs

### Email Operations
- **POST** `/api/send-results` - Send results to students with email config
- **POST** `/api/test-email-config` - Test email configuration
- **GET** `/api/email-logs` - Get all email logs
- **GET** `/api/email-logs/export` - Export logs as CSV

### Sharing
- **POST** `/api/share/create` - Create shareable link
- **GET** `/api/share/<token>` - Get shared results
- **POST** `/api/share/<token>/deactivate` - Deactivate share link
- **GET** `/api/shares` - Get all active shares

### Help & Support
- **GET** `/api/help-faqs` - Get FAQ list

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
    student_id VARCHAR(50),           -- Optional student ID
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    score FLOAT NOT NULL,
    subject VARCHAR(120),
    batch VARCHAR(50),
    comment TEXT,                     -- Teacher comments
    extra_data JSON,                  -- Dynamic fields from uploaded file
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Email Logs Table
```sql
CREATE TABLE email_logs (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'sent', 'failed'
    error_message TEXT,
    sent_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
```

### Shared Results Table
```sql
CREATE TABLE shared_results (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    share_token VARCHAR(100) UNIQUE NOT NULL,
    shared_with_email VARCHAR(120) NOT NULL,
    shared_by VARCHAR(120),
    expires_at DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    view_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_viewed_at DATETIME,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
```

## 🎨 Customization

### Change Email Template
Edit the `send_email_to_student()` function in `email_service.py` to customize:
- Email subject line
- HTML layout and styling
- Color schemes for score ranges
- Encouragement messages
- Table formatting

### Modify UI Colors
Edit the Tailwind CSS classes in template files (`templates/*.html`) to change:
- Navigation bar colors
- Button styles
- Card backgrounds
- Text colors

### Add Custom Fields
No code changes needed! The system automatically:
- Detects and stores any extra columns from uploaded files
- Displays them in the email template
- Preserves column order from the original file

### Change Timezone
Edit `BANGKOK_TZ` in `models.py` and `email_service.py` to use a different timezone:
```python
BANGKOK_TZ = pytz.timezone('Asia/Bangkok')  # Change to your timezone
```

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

**Version**: 2.0.0  
**Last Updated**: November 2024  
**Status**: Production Ready  
**Author**: Ny Seyha  
**License**: Open Source

