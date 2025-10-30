# Testing Guide - Send Student Result System

This guide provides comprehensive testing procedures to ensure all features work correctly.

## Pre-Testing Setup

1. Ensure the application is running: `python app.py`
2. Open browser to: `http://localhost:5000`
3. Have the sample CSV file ready: `sample_data.csv`

## Test Cases

### Test 1: File Upload Functionality

**Objective:** Verify that CSV files can be uploaded and validated correctly

**Steps:**
1. Navigate to the home page (Upload section)
2. Click on the upload area
3. Select `sample_data.csv`
4. Click "Upload File"

**Expected Results:**
- ✅ File is accepted
- ✅ Success message appears
- ✅ Data is parsed correctly
- ✅ Redirected to preview page
- ✅ Student count matches file

**Test Data:**
```csv
name,email,score,subject,batch
John Doe,john@example.com,85.5,Mathematics,2024-A
Jane Smith,jane@example.com,92.0,Physics,2024-B
```

### Test 2: File Validation

**Objective:** Verify that invalid files are rejected

**Test Cases:**

#### 2a: Missing Required Columns
**File Content:**
```csv
name,email
John Doe,john@example.com
```

**Expected Result:**
- ❌ Error message: "Missing required columns: score"

#### 2b: Invalid File Format
**File:** test.txt or test.pdf

**Expected Result:**
- ❌ Error message: "Invalid file format"

#### 2c: Empty File
**File:** empty.csv

**Expected Result:**
- ❌ Error message or empty data handling

### Test 3: Data Preview

**Objective:** Verify preview page displays data correctly

**Steps:**
1. Upload sample_data.csv
2. Review the preview page

**Expected Results:**
- ✅ All students displayed in table
- ✅ Statistics show correct counts
- ✅ Average score calculated correctly
- ✅ Search functionality works
- ✅ Checkboxes for selection work

**Verification:**
- Total Students: 10
- Valid Emails: 10
- Average Score: 88.35

### Test 4: Search Functionality

**Objective:** Verify search filters work correctly

**Steps:**
1. On preview page, enter "John" in search box
2. Verify only John Doe appears
3. Clear search and try "example.com"
4. Verify all students with that domain appear

**Expected Results:**
- ✅ Search is case-insensitive
- ✅ Filters by name and email
- ✅ Results update in real-time

### Test 5: Student Selection

**Objective:** Verify checkbox selection works

**Steps:**
1. Click "Select All" checkbox
2. Verify all rows are selected
3. Click "Select All" again
4. Verify all rows are deselected
5. Select individual students

**Expected Results:**
- ✅ All checkboxes toggle together
- ✅ Individual selection works
- ✅ "Send Selected" button enables/disables correctly

### Test 6: Email Sending (Test Mode)

**Objective:** Verify email sending functionality

**Prerequisites:**
- Email configuration in `.env` is correct
- Test email account is set up

**Steps:**
1. On preview page, select 1-2 students
2. Click "Send Selected"
3. Confirm in dialog
4. Monitor sending progress

**Expected Results:**
- ✅ Sending starts immediately
- ✅ Progress updates in real-time
- ✅ Redirects to logs page
- ✅ Emails appear in recipient inbox

**Verification:**
- Check recipient email inbox
- Verify email contains student name
- Verify email contains score
- Verify email is properly formatted

### Test 7: Email Logs

**Objective:** Verify email logs are recorded correctly

**Steps:**
1. Navigate to Logs page
2. Review the email log table
3. Filter by status
4. Search for specific student

**Expected Results:**
- ✅ All sent emails appear in logs
- ✅ Status shows "sent" or "failed"
- ✅ Sent timestamp is recorded
- ✅ Filter by status works
- ✅ Search functionality works

### Test 8: Log Export

**Objective:** Verify logs can be exported as CSV

**Steps:**
1. On Logs page, click "Export CSV"
2. Check downloads folder

**Expected Results:**
- ✅ CSV file is generated
- ✅ File contains all log data
- ✅ Filename includes timestamp

### Test 9: Statistics

**Objective:** Verify statistics are calculated correctly

**Steps:**
1. Upload sample data
2. Check preview page statistics
3. Send emails
4. Check logs page statistics

**Expected Results:**
- ✅ Total Students: 10
- ✅ Valid Emails: 10
- ✅ Average Score: 88.35
- ✅ Sent count increases after sending
- ✅ Failed count shows any failures

### Test 10: Error Handling

**Objective:** Verify error handling works correctly

**Test Cases:**

#### 10a: Invalid Email Address
**File Content:**
```csv
name,email,score
John Doe,invalid-email,85.5
```

**Expected Result:**
- ⚠️ Email validation error or sending failure logged

#### 10b: Invalid Score
**File Content:**
```csv
name,email,score
John Doe,john@example.com,not-a-number
```

**Expected Result:**
- ❌ Error message: "Score must be numeric"

#### 10c: Network Error Simulation
**Steps:**
1. Disconnect internet
2. Try to send email
3. Reconnect internet

**Expected Result:**
- ✅ Error is caught and logged
- ✅ Error message displayed to user

### Test 11: Responsive Design

**Objective:** Verify UI works on different screen sizes

**Steps:**
1. Open browser DevTools (F12)
2. Test on different device sizes:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1920px)

**Expected Results:**
- ✅ Layout adapts to screen size
- ✅ All buttons are clickable
- ✅ Tables are scrollable on mobile
- ✅ Navigation works on all sizes

### Test 12: Navigation

**Objective:** Verify navigation between pages works

**Steps:**
1. Click on "Upload" in navigation
2. Click on "Preview"
3. Click on "Logs"
4. Use back buttons

**Expected Results:**
- ✅ All navigation links work
- ✅ Page content loads correctly
- ✅ Data persists between pages

### Test 13: Database Operations

**Objective:** Verify database operations work correctly

**Steps:**
1. Upload data
2. Check database file exists
3. Upload different data
4. Verify old data is replaced

**Expected Results:**
- ✅ `student_results.db` file created
- ✅ Data is persisted
- ✅ Database can be queried

### Test 14: Performance

**Objective:** Verify system performs well with larger datasets

**Test Data:** Create CSV with 100+ students

**Steps:**
1. Upload large CSV file
2. Monitor page load time
3. Send emails to all students
4. Monitor sending time

**Expected Results:**
- ✅ Upload completes in < 5 seconds
- ✅ Preview page loads in < 2 seconds
- ✅ Sending completes without errors
- ✅ No memory leaks

### Test 15: Security

**Objective:** Verify security measures are in place

**Test Cases:**

#### 15a: File Upload Security
**Steps:**
1. Try uploading executable file (.exe)
2. Try uploading large file (> 16MB)

**Expected Results:**
- ❌ File rejected with error message

#### 15b: SQL Injection
**Steps:**
1. Try entering SQL in search box
2. Try entering SQL in email field

**Expected Results:**
- ✅ Input is sanitized
- ✅ No SQL injection possible

## Test Results Template

```
Test Case: [Test Name]
Date: [Date]
Tester: [Name]
Status: [PASS/FAIL]
Notes: [Any observations]

Expected Results:
- [ ] Result 1
- [ ] Result 2

Actual Results:
- [ ] Result 1
- [ ] Result 2

Issues Found:
- [Issue 1]
- [Issue 2]
```

## Automated Testing (Optional)

### Unit Tests

Create `test_app.py`:

```python
import unittest
from app import app, db
from models import Student, EmailLog

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def test_health_check(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
    
    def test_upload_endpoint(self):
        response = self.app.post('/api/upload')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest test_app.py
```

## Performance Benchmarks

| Operation | Expected Time | Actual Time | Status |
|-----------|---------------|------------|--------|
| File Upload (10 students) | < 2s | | |
| File Upload (100 students) | < 5s | | |
| Preview Page Load | < 1s | | |
| Send 10 Emails | < 10s | | |
| Send 100 Emails | < 60s | | |
| Export Logs | < 2s | | |

## Known Issues & Workarounds

### Issue: Emails not sending
**Workaround:** Check `.env` configuration and email account settings

### Issue: Database locked
**Workaround:** Delete `student_results.db` and restart application

### Issue: Port 5000 in use
**Workaround:** Change port in `app.py` or kill process using port 5000

## Sign-Off

- [ ] All tests passed
- [ ] No critical issues found
- [ ] Performance acceptable
- [ ] Security verified
- [ ] Ready for production

**Tested By:** ________________  
**Date:** ________________  
**Approved By:** ________________

---

**Testing Status:** Ready for Production ✅

