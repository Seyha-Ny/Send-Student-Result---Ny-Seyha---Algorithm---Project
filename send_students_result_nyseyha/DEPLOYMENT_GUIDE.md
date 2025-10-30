# Deployment Guide - Send Student Result System

This guide provides instructions for deploying the Send Student Result System to production environments.

## Deployment Options

### Option 1: Local/On-Premises Deployment

#### Requirements
- Windows/Linux/macOS server
- Python 3.8+
- Gunicorn or uWSGI (WSGI server)
- Nginx or Apache (reverse proxy)
- SSL certificate (for HTTPS)

#### Steps

1. **Install Dependencies**
```bash
pip install -r requirements.txt
pip install gunicorn
```

2. **Create Production .env**
```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=sqlite:///student_results.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=noreply@studentresults.com
```

3. **Run with Gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

4. **Configure Nginx (Reverse Proxy)**
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Enable HTTPS with Let's Encrypt**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

### Option 2: Cloud Deployment (Heroku)

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps

1. **Create Procfile**
```
web: gunicorn app:app
```

2. **Create runtime.txt**
```
python-3.11.0
```

3. **Initialize Git Repository**
```bash
git init
git add .
git commit -m "Initial commit"
```

4. **Deploy to Heroku**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

5. **Set Environment Variables**
```bash
heroku config:set MAIL_SERVER=smtp.gmail.com
heroku config:set MAIL_USERNAME=your_email@gmail.com
heroku config:set MAIL_PASSWORD=your_app_password
```

6. **Initialize Database**
```bash
heroku run python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Option 3: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - MAIL_SERVER=smtp.gmail.com
      - MAIL_USERNAME=${MAIL_USERNAME}
      - MAIL_PASSWORD=${MAIL_PASSWORD}
    volumes:
      - ./uploads:/app/uploads
      - ./student_results.db:/app/student_results.db
```

#### Build and Run
```bash
docker-compose up -d
```

### Option 4: AWS Deployment (Elastic Beanstalk)

#### Steps

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB Application**
```bash
eb init -p python-3.11 student-results-app
```

3. **Create Environment**
```bash
eb create production-env
```

4. **Set Environment Variables**
```bash
eb setenv MAIL_SERVER=smtp.gmail.com MAIL_USERNAME=your_email@gmail.com
```

5. **Deploy**
```bash
eb deploy
```

### Option 5: PythonAnywhere Deployment

#### Steps

1. **Create Account** at pythonanywhere.com

2. **Upload Files**
   - Use web interface to upload project files

3. **Create Virtual Environment**
   - Use PythonAnywhere console

4. **Configure Web App**
   - Set Python version to 3.11
   - Set WSGI configuration file

5. **Set Environment Variables**
   - Add to WSGI file or environment

6. **Reload Web App**
   - Click "Reload" button

## Production Checklist

### Security
- [ ] Change DEBUG to False
- [ ] Set SECRET_KEY in production
- [ ] Use HTTPS/SSL certificate
- [ ] Enable CSRF protection
- [ ] Validate all user inputs
- [ ] Use strong database passwords
- [ ] Restrict file upload types
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Use environment variables for secrets

### Performance
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Set up reverse proxy (Nginx, Apache)
- [ ] Enable caching headers
- [ ] Optimize database queries
- [ ] Use CDN for static files
- [ ] Monitor server resources
- [ ] Set up load balancing (if needed)

### Database
- [ ] Use PostgreSQL or MySQL (not SQLite)
- [ ] Set up database backups
- [ ] Enable database encryption
- [ ] Create database indexes
- [ ] Monitor database performance
- [ ] Set up database replication (if needed)

### Monitoring & Logging
- [ ] Set up error logging
- [ ] Monitor application performance
- [ ] Set up uptime monitoring
- [ ] Create backup strategy
- [ ] Monitor email delivery
- [ ] Set up alerts for failures

### Maintenance
- [ ] Document deployment process
- [ ] Create rollback procedure
- [ ] Set up automated backups
- [ ] Plan for updates
- [ ] Monitor security patches
- [ ] Test disaster recovery

## Database Migration (SQLite to PostgreSQL)

### Step 1: Export Data from SQLite
```python
import sqlite3
import json

conn = sqlite3.connect('student_results.db')
cursor = conn.cursor()

# Export students
cursor.execute('SELECT * FROM students')
students = cursor.fetchall()

# Export email logs
cursor.execute('SELECT * FROM email_logs')
logs = cursor.fetchall()

conn.close()
```

### Step 2: Update Configuration
```env
DATABASE_URL=postgresql://user:password@localhost/student_results
```

### Step 3: Create Tables in PostgreSQL
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Step 4: Import Data
```python
from app import app, db
from models import Student, EmailLog

with app.app_context():
    # Import students
    for student_data in students:
        student = Student(...)
        db.session.add(student)
    
    db.session.commit()
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (AWS ELB, Nginx)
- Deploy multiple application instances
- Use shared database
- Use shared file storage (S3, NFS)

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize application code
- Use caching (Redis, Memcached)
- Optimize database queries

### Email Sending at Scale
- Use task queue (Celery, RQ)
- Implement email batching
- Use email service provider (SendGrid, AWS SES)
- Monitor email delivery rates

## Monitoring & Maintenance

### Key Metrics to Monitor
- Application response time
- Error rate
- Email delivery success rate
- Database query performance
- Server resource usage
- Uptime percentage

### Tools
- **Monitoring**: Prometheus, Grafana, New Relic
- **Logging**: ELK Stack, Splunk, CloudWatch
- **Error Tracking**: Sentry, Rollbar
- **Performance**: DataDog, Dynatrace

### Backup Strategy
- Daily automated backups
- Store backups in multiple locations
- Test backup restoration regularly
- Keep backup retention policy

## Troubleshooting Production Issues

### Issue: Application Crashes
**Solution:**
- Check error logs
- Verify environment variables
- Check database connection
- Restart application

### Issue: Slow Email Sending
**Solution:**
- Use task queue (Celery)
- Implement email batching
- Check SMTP server performance
- Use email service provider

### Issue: Database Performance
**Solution:**
- Add database indexes
- Optimize queries
- Archive old logs
- Use database replication

### Issue: High Memory Usage
**Solution:**
- Increase server resources
- Optimize code
- Use caching
- Monitor for memory leaks

## Rollback Procedure

1. **Identify Issue**
   - Check logs and monitoring
   - Determine root cause

2. **Prepare Rollback**
   - Have previous version ready
   - Backup current database

3. **Execute Rollback**
   - Stop current application
   - Deploy previous version
   - Verify functionality

4. **Post-Rollback**
   - Monitor application
   - Investigate issue
   - Plan fix

## Support & Help

- Check application logs
- Review monitoring dashboards
- Contact hosting provider support
- Review deployment documentation

---

**Deployment Status:** Ready for Production ✅

