# 📧 Email Setup & Testing Guide

## 🎯 Goal
Send student results via email using your Gmail account with Python

---

## ✅ Step 1: Get Gmail App Password

### Why App Password?
Gmail requires an **App Password** (not your regular password) for security.

### How to Get It:

1. **Enable 2-Step Verification**:
   - Go to: https://myaccount.google.com/signinoptions/two-step-verification
   - Follow the steps to enable it
   - This is REQUIRED before you can create App Passwords

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select:
     - **App**: Mail
     - **Device**: Other (Custom name) → Type "Student Results"
   - Click **Generate**
   - Copy the **16-character password** (e.g., `abcd efgh ijkl mnop`)
   - **IMPORTANT**: Save this password! You'll need it every time.

---

## 🧪 Step 2: Test Email Sending

### Option A: Use Test Script (Recommended)

1. **Run the test script**:
   ```powershell
   python test_email.py
   ```

2. **Enter when prompted**:
   - Your Gmail address: `youremail@gmail.com`
   - Your App Password: `abcdefghijklmnop` (16 chars, no spaces)
   - Test recipient: `youremail@gmail.com` (can be same as sender)

3. **Check results**:
   - ✅ **Success**: "Email sent successfully!" → Your config works!
   - ❌ **Failed**: See error message and fix below

### Option B: Test in the App

1. **Open the app**: http://127.0.0.1:5000

2. **Look at right sidebar**: "Gmail Configuration"

3. **Enter credentials**:
   - Sender Email: `youremail@gmail.com`
   - App Password: `your-16-char-password`

4. **Click "Test Email Configuration"**

5. **Check result**:
   - ✅ Green success message → Works!
   - ❌ Red error message → See fixes below

---

## ❌ Common Errors & Fixes

### Error 1: "Authentication Failed" or "Username and Password not accepted"

**Cause**: Wrong password or not using App Password

**Fix**:
1. Make sure you're using **App Password**, NOT regular Gmail password
2. Generate new App Password: https://myaccount.google.com/apppasswords
3. Enable 2-Step Verification first if not enabled
4. Copy the 16-character password exactly (remove spaces)
5. Try again

---

### Error 2: "SMTP AUTH extension not supported by server"

**Cause**: TLS not enabled or wrong port

**Fix**:
1. Make sure using port **587** (not 465 or 25)
2. TLS must be enabled
3. Check `.env` file has:
   ```
   MAIL_PORT=587
   MAIL_USE_TLS=True
   ```

---

### Error 3: "Connection refused" or "Timeout"

**Cause**: Firewall blocking or no internet

**Fix**:
1. Check internet connection
2. Try disabling firewall temporarily
3. Check if port 587 is blocked
4. Try from different network

---

### Error 4: "Sender address rejected"

**Cause**: Email address doesn't match authenticated account

**Fix**:
1. Make sure sender email matches the Gmail account you're logging in with
2. Both must be the same Gmail address

---

## 📝 How Email Sending Works in Your App

### Flow:

```
1. User enters Gmail + App Password
   ↓
2. App validates credentials (Test button)
   ↓
3. User uploads students
   ↓
4. User goes to Preview page
   ↓
5. User enters credentials again
   ↓
6. User clicks "Send All Results"
   ↓
7. App temporarily uses your Gmail credentials
   ↓
8. Python sends emails via Gmail SMTP
   ↓
9. Students receive emails FROM your Gmail
   ↓
10. App restores original config
```

### Technical Details:

- **SMTP Server**: smtp.gmail.com
- **Port**: 587
- **Security**: TLS encryption
- **Authentication**: Gmail + App Password
- **Library**: Flask-Mail (uses Python smtplib)

---

## 🔧 Configuration Files

### `.env` File (Server Default - Optional)

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

**Note**: This is only used as fallback. The app now REQUIRES sender to enter credentials.

### `app.py` (Flask-Mail Setup)

```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = sender_email  # From user input
app.config['MAIL_PASSWORD'] = app_password  # From user input
```

---

## ✅ Verification Checklist

Before sending to students, verify:

- [ ] 2-Step Verification enabled on Gmail
- [ ] App Password generated and saved
- [ ] Test script runs successfully
- [ ] Test email configuration in app shows ✅
- [ ] Received test email in inbox
- [ ] Email appears FROM your Gmail address
- [ ] No authentication errors

---

## 🎯 Send Your First Student Result

1. **Prepare CSV file**:
   ```csv
   name,email,score,subject,batch
   Test Student,your-email@gmail.com,95,Test,Batch A
   ```

2. **Upload to app**:
   - Enter Gmail + App Password
   - Test configuration ✅
   - Upload CSV file
   - Auto-redirects to Preview

3. **Send**:
   - Enter App Password in orange box
   - Click "Send All Results"
   - Confirm
   - Check Logs page

4. **Verify**:
   - Check your email inbox
   - Should receive beautiful HTML email
   - FROM your Gmail address
   - With score and subject info

---

## 🔒 Security Notes

1. **App Password is NOT stored** on server
2. **Only used temporarily** during send
3. **Never share** your App Password
4. **Revoke** if compromised: https://myaccount.google.com/apppasswords
5. **Generate new** if you forget it

---

## 📊 Email Limits

### Gmail Sending Limits:

- **Per day**: 500 emails (for regular Gmail)
- **Per minute**: ~20-30 emails
- **Recommendation**: Send in batches of 50-100

### If You Hit Limits:

1. Wait 24 hours
2. Send smaller batches
3. Use Google Workspace for higher limits
4. Consider using dedicated email service (SendGrid, etc.)

---

## 🆘 Still Not Working?

### Debug Steps:

1. **Run test script**:
   ```powershell
   python test_email.py
   ```

2. **Check terminal output** for errors

3. **Verify credentials**:
   - Email address is correct
   - App Password is 16 characters
   - No extra spaces

4. **Try different email**:
   - Send to different recipient
   - Check spam folder

5. **Check Gmail settings**:
   - 2-Step Verification enabled
   - App Password still valid
   - IMAP/SMTP access allowed

---

## 📞 Resources

- **Generate App Password**: https://myaccount.google.com/apppasswords
- **Enable 2-Step**: https://myaccount.google.com/signinoptions/two-step-verification
- **Gmail SMTP Info**: https://support.google.com/mail/answer/7126229
- **Test Script**: `test_email.py` in project folder
- **Help Page**: http://127.0.0.1:5000/help

---

## ✅ Success Indicators

You'll know it's working when:

- ✅ Test script shows "Email sent successfully!"
- ✅ App shows green "Configuration valid" message
- ✅ Test email arrives in inbox
- ✅ Logs page shows "Sent" count increasing
- ✅ Students receive emails FROM your Gmail
- ✅ No authentication errors

---

**Your email sending is now configured! Use `test_email.py` to verify, then send student results through the app.** 🚀
