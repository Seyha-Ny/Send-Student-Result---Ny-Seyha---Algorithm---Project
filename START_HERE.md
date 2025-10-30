# 🚀 START HERE - Quick Start Guide

## 📧 Your Student Results Email System

Send student results via email using Python and Gmail!

---

## ⚡ Quick Start (5 Minutes)

### 1. Test Email First

```powershell
python test_email.py
```

Enter your Gmail and App Password when prompted. If successful, you're ready!

### 2. Open the App

```powershell
python app.py
```

Then open: http://127.0.0.1:5000

### 3. Send Results

1. Enter Gmail + App Password (right sidebar)
2. Upload `sample_students.csv`
3. Click "Send All Results"
4. Done! ✅

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `EMAIL_SETUP_GUIDE.md` | **How to setup Gmail for sending emails** |
| `QUICK_FIX.md` | **Fix CSV column errors** |
| `HOW_TO_USE.md` | **Complete usage guide** |
| `CHANGES_SUMMARY.md` | **What changed in the app** |
| `sample_students.csv` | **Template CSV file** |
| `test_email.py` | **Test email sending** |

---

## 🎯 Common Tasks

### Test if Email Works
```powershell
python test_email.py
```

### Start the App
```powershell
python app.py
```
Then go to: http://127.0.0.1:5000

### Fix CSV File Errors
Read: `QUICK_FIX.md`

### Setup Gmail
Read: `EMAIL_SETUP_GUIDE.md`

---

## ❓ Quick Troubleshooting

### ❌ "Authentication Failed"
→ Read `EMAIL_SETUP_GUIDE.md` → Get Gmail App Password

### ❌ "File must have columns: name, email, score"
→ Read `QUICK_FIX.md` → Fix CSV column names

### ❌ "Students not showing"
→ Refresh Preview page → Check database file exists

### ❌ "Can't send emails"
→ Run `python test_email.py` → Follow error messages

---

## 📋 Requirements

- Python 3.7+
- Gmail account with 2-Step Verification
- Gmail App Password
- CSV file with columns: `name,email,score,subject,batch`

---

## 🔐 Gmail App Password

**Required for sending emails!**

1. Enable 2-Step Verification: https://myaccount.google.com/signinoptions/two-step-verification
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Copy the 16-character password
4. Use it in the app (NOT your regular Gmail password)

---

## ✅ Success Checklist

- [ ] Ran `python test_email.py` successfully
- [ ] Got Gmail App Password
- [ ] Started app with `python app.py`
- [ ] Opened http://127.0.0.1:5000
- [ ] Tested email configuration ✅
- [ ] Uploaded `sample_students.csv`
- [ ] Sent test results
- [ ] Checked Logs page
- [ ] Received email in inbox

---

## 🆘 Need Help?

1. **Email issues**: Read `EMAIL_SETUP_GUIDE.md`
2. **CSV issues**: Read `QUICK_FIX.md`
3. **Usage help**: Read `HOW_TO_USE.md`
4. **In-app help**: Click "Help" in navigation

---

## 📞 Quick Links

- **App**: http://127.0.0.1:5000
- **Help Page**: http://127.0.0.1:5000/help
- **Gmail App Passwords**: https://myaccount.google.com/apppasswords
- **Enable 2-Step**: https://myaccount.google.com/signinoptions/two-step-verification

---

**Ready? Run `python test_email.py` to test email, then `python app.py` to start!** 🚀
