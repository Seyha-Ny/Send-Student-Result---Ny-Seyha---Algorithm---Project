# 🔧 Quick Fix - Column Names Error

## ❌ Error You're Getting

```
File must have these columns: name, email, score. 
Missing: name, email, score.
```

## ✅ Solution

Your CSV file column names are **NOT lowercase** or **NOT exact**.

### Fix Your CSV File

**Open your CSV file and make sure the FIRST ROW looks EXACTLY like this:**

```csv
name,email,score,subject,batch
```

**IMPORTANT:**
- ✅ All lowercase: `name` not `Name` or `NAME`
- ✅ No spaces: `name` not `name ` or ` name`
- ✅ Exact spelling: `email` not `Email` or `e-mail`
- ✅ Comma separated, no extra commas

---

## 📝 Example of CORRECT CSV File

```csv
name,email,score,subject,batch
John Smith,john@example.com,85,Math,Batch A
Sarah Lee,sarah@example.com,92,Physics,Batch B
```

**First line = column names (lowercase)**  
**Second line onwards = student data**

---

## 📝 Example of WRONG CSV Files

### ❌ WRONG - Uppercase columns
```csv
Name,Email,Score,Subject,Batch
John Smith,john@example.com,85,Math,Batch A
```

### ❌ WRONG - Mixed case
```csv
Name,email,Score,subject,batch
John Smith,john@example.com,85,Math,Batch A
```

### ❌ WRONG - Different column names
```csv
student_name,student_email,marks,course,class
John Smith,john@example.com,85,Math,Batch A
```

### ❌ WRONG - No header row
```csv
John Smith,john@example.com,85,Math,Batch A
Sarah Lee,sarah@example.com,92,Physics,Batch B
```

---

## 🎯 Quick Steps to Fix

### Option 1: Use the Sample File (EASIEST)

1. **Find the file**: `sample_students.csv` in your project folder
2. **Open it** in Excel or Notepad
3. **Copy your student data** into it (keep the first row as-is)
4. **Save** and upload

### Option 2: Fix Your Existing File

1. **Open your CSV file** in Excel or Notepad
2. **Look at the first row** (the header row)
3. **Change it to EXACTLY**: `name,email,score,subject,batch`
4. **Make sure it's lowercase**
5. **Save** the file
6. **Upload again**

### Option 3: Create New File in Excel

1. **Open Excel**
2. **First row** (A1 to E1):
   - A1: `name`
   - B1: `email`
   - C1: `score`
   - D1: `subject`
   - E1: `batch`
3. **Add your student data** starting from row 2
4. **Save As** → CSV (Comma delimited)
5. **Upload**

---

## 🔍 How to Check Your File

### In Notepad:
1. Right-click your CSV file
2. Open with Notepad
3. First line should be: `name,email,score,subject,batch`
4. All lowercase, no spaces

### In Excel:
1. Open your CSV file
2. First row should have: `name` `email` `score` `subject` `batch`
3. All lowercase
4. When you save, choose "CSV (Comma delimited)"

---

## ✅ After Fixing

1. **Save your file**
2. **Go to the app**: http://127.0.0.1:5000
3. **Upload the fixed file**
4. **Should work now!** ✅

---

## 💡 Pro Tip

**Always use the `sample_students.csv` file as your template!**

1. Copy `sample_students.csv`
2. Rename it to `my_students.csv`
3. Replace the sample data with your students
4. Keep the first row unchanged
5. Upload

---

## 🆘 Still Not Working?

**Check these:**

- [ ] First row is: `name,email,score,subject,batch`
- [ ] All lowercase letters
- [ ] No extra spaces before or after column names
- [ ] File is saved as CSV format
- [ ] No empty rows at the top
- [ ] Columns separated by commas, not semicolons or tabs

**If still failing, the error message will now show:**
- What columns your file has
- What columns are missing
- Use that info to fix your file

---

## 📞 Need Help?

1. Check the `sample_students.csv` file
2. Read `HOW_TO_USE.md` for complete guide
3. Visit Help page: http://127.0.0.1:5000/help
