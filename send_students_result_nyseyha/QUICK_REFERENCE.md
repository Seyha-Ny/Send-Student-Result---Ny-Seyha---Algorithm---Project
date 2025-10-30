# Quick Reference Guide - Send Student Result System

## 🚀 Quick Start (30 seconds)

### Windows
```bash
quickstart.bat
```

### macOS/Linux
```bash
chmod +x quickstart.sh
./quickstart.sh
```

Then open: **http://localhost:5000**

## 📋 File Format

```csv
name,email,score,subject,batch
John Doe,john@example.com,85.5,Mathematics,2024-A
Jane Smith,jane@example.com,92.0,Physics,2024-B
```

**Required**: name, email, score  
**Optional**: subject, batch

## 🔧 Email Configuration

### Gmail (Recommended)
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

**Steps:**
1. Enable 2-Factor Authentication
2. Go to https://myaccount.google.com/apppasswords
3. Generate App Password
4. Copy to .env file

### Outlook
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USERNAME=your_email@outlook.com
MAIL_PASSWORD=your_password
```

### SendGrid
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.your_api_key
```

## 🌐 Pages

| Page | URL | Purpose |
|------|-----|---------|
| Upload | http://localhost:5000/ | Upload CSV/Excel files |
| Preview | http://localhost:5000/preview | Review and send emails |
| Logs | http://localhost:5000/logs | Track email delivery |

## 🔌 API Endpoints

```
POST   /api/upload              - Upload file
POST   /api/save-students       - Save to database
GET    /api/students            - Get all students
POST   /api/send-results        - Send emails
GET    /api/email-logs          - Get logs
GET    /api/email-logs/export   - Export CSV
GET    /api/health              - Health check
```

## 📁 Project Files

```
app.py                 - Main application
models.py              - Database models
routes.py              - API endpoints
email_service.py       - Email logic
utils.py               - Utilities
requirements.txt       - Dependencies
.env.example           - Config template
sample_data.csv        - Sample data
templates/             - HTML templates
```

## 🐛 Troubleshooting

### SMTP Authentication Failed
- Check email and password in .env
- For Gmail, use App Password (not regular password)
- Enable 2-Factor Authentication

### File Upload Failed
- Ensure CSV or Excel format
- Check required columns: name, email, score
- File size < 16MB

### Database Error
- Delete student_results.db
- Restart application

### Port 5000 Already in Use
- Edit app.py: change port=5000 to port=5001

## 📊 Statistics

| Metric | Location |
|--------|----------|
| Total Students | Preview page |
| Valid Emails | Preview page |
| Average Score | Preview page |
| Emails Sent | Logs page |
| Emails Failed | Logs page |
| Emails Pending | Logs page |

## 🎯 Workflow

```
1. Upload CSV/Excel
   ↓
2. Review Preview
   ↓
3. Select Students
   ↓
4. Send Emails
   ↓
5. Check Logs
   ↓
6. Export Results
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| README.md | Full documentation |
| SETUP_GUIDE.md | Installation steps |
| TESTING_GUIDE.md | Testing procedures |
| DEPLOYMENT_GUIDE.md | Production deployment |
| PROJECT_SUMMARY.md | Project overview |
| CHECKLIST.md | Completion checklist |

## 🔒 Security Tips

- Never commit .env file
- Use strong passwords
- Keep dependencies updated
- Use HTTPS in production
- Validate all inputs

## 💡 Tips & Tricks

### Search
- Search by name or email
- Case-insensitive
- Real-time filtering

### Selection
- Click checkbox to select individual
- Click "Select All" to select all
- "Send Selected" for partial sending

### Logs
- Auto-refreshes every 30 seconds
- Filter by status (Sent, Failed, Pending)
- Export as CSV for records

### Email Template
- Edit in email_service.py
- Customize HTML
- Add custom fields

## 🚀 Deployment

### Local
```bash
python app.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```bash
docker-compose up -d
```

### Heroku
```bash
git push heroku main
```

## 📞 Common Commands

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Initialize database
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

## 🎓 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Tailwind CSS: https://tailwindcss.com/
- Flask-Mail: https://pythonhosted.org/Flask-Mail/

## 📈 Performance Tips

- Use PostgreSQL for production (not SQLite)
- Implement async email sending (Celery)
- Add caching (Redis)
- Use CDN for static files
- Monitor with tools like Sentry

## 🔄 Workflow Examples

### Example 1: Send to All Students
1. Upload file
2. Click "Send All Results"
3. Confirm
4. Check logs

### Example 2: Send to Selected Students
1. Upload file
2. Go to Preview
3. Select specific students
4. Click "Send Selected"
5. Confirm
6. Check logs

### Example 3: Export Results
1. Go to Logs page
2. Click "Export CSV"
3. File downloads
4. Open in Excel

## 🎯 Best Practices

1. **Always preview data** before sending
2. **Test with sample data** first
3. **Keep backups** of logs
4. **Monitor email delivery** status
5. **Update dependencies** regularly
6. **Use strong passwords** for email
7. **Enable 2FA** on email account
8. **Document custom changes**

## 📞 Support

- Check README.md for features
- Check SETUP_GUIDE.md for installation
- Check TESTING_GUIDE.md for testing
- Check DEPLOYMENT_GUIDE.md for deployment
- Review error messages in logs

## ✅ Checklist Before Sending

- [ ] File uploaded successfully
- [ ] Data preview looks correct
- [ ] Email addresses are valid
- [ ] Scores are correct
- [ ] Email configuration is set
- [ ] Test email sent successfully
- [ ] Ready to send to all students

## 🎉 You're Ready!

The Send Student Result System is ready to use. Start by uploading your first CSV file and sending results to your students!

---

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Last Updated**: 2024

