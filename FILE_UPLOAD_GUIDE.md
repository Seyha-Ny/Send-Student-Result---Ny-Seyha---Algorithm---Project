# 📁 File Upload Format Guide

## Quick Start

### ✅ What You Need
**Only 1 column is required**: `email`

**Everything else is optional!**

---

## 📊 Upload ANY Format You Want

The system is **completely flexible**. You can upload files with ANY columns, and they will ALL appear in the email table.

### Example 1: Minimal Format
```csv
email
student1@example.com
student2@example.com
```

### Example 2: Basic Format
```csv
name,email,score
John Doe,john@example.com,85
Jane Smith,jane@example.com,92
```

### Example 3: Your Current Format
```csv
first name,last name,id,class,email,hw1,participation,q1,final khmer,final english,total,grade,comments
John,Doe,2001,CS101,john@example.com,85,90,88,92,89,88.8,A,Excellent work
Jane,Smith,2002,CS101,jane@example.com,78,85,82,80,85,82.0,B+,Good progress
```

### Example 4: Custom Format
```csv
email,quiz1,quiz2,quiz3,midterm,final,project,attendance,total,grade,teacher_notes
john@example.com,80,85,90,88,92,95,100,89.5,A,Outstanding student
jane@example.com,75,80,85,82,88,90,95,85.2,B+,Very good work
```

---

## 🎯 How It Works

### 1. Column Recognition
The system automatically recognizes these standard columns:
- `email` ← **REQUIRED**
- `name` or `first name` + `last name`
- `score` or `total`
- `id` or `student_id`
- `class` or `batch`
- `subject`
- `comment` or `comments`

### 2. Extra Columns
**ANY other columns** you add will:
- ✅ Be stored in the database
- ✅ Appear in the email table
- ✅ Display in the SAME ORDER as your file
- ✅ Be preserved for future use

### 3. Column Order
The email table will show columns in the **exact same order** as your CSV file (excluding email, which is used for sending).

**Your CSV**:
```
first name, last name, id, class, hw1, total, grade
```

**Email Table**:
```
FIRST NAME | LAST NAME | ID | CLASS | HW1 | TOTAL | GRADE
```

---

## 💬 Comments Feature

### Option 1: Add Comments in CSV
```csv
email,score,comments
john@example.com,85,Excellent work! Keep it up.
jane@example.com,78,Good progress this semester.
```

### Option 2: Add Comments in App
1. Upload your CSV file (with or without comments)
2. Go to Preview page
3. Type comments in the "Comment" column
4. Comments are saved automatically
5. They will appear in the email table

### Both Options Work Together!
- Upload CSV with some comments
- Edit or add more comments in the app
- All comments will be included in emails

---

## 📋 Supported File Types

- ✅ **CSV** (.csv)
- ✅ **Excel** (.xlsx, .xls)

---

## ⚠️ Important Notes

### Required Field
- `email` column is **REQUIRED**
- Without it, the file will be rejected

### Column Names
- Column names are **case-insensitive**
  - `Email`, `email`, `EMAIL` all work
  - `First Name`, `first name`, `FIRST NAME` all work

### Auto-Mapping
System automatically handles common variations:
- `comments` → `comment`
- `first name` + `last name` → `name`
- `class` → `batch`
- `id` → `student_id`

### Missing Data
- Empty cells are allowed
- Students with missing email will be skipped
- Other missing fields will show as empty in emails

---

## 🎨 Email Table Styling

### Highlighted Columns
These columns get special highlighting (yellow background):
- `total`
- `grade`
- `score`

### All Other Columns
- Display with normal styling
- Still included in the table
- Easy to read and scan

---

## 🚀 Best Practices

### 1. Organize Your Columns
Put columns in the order you want students to see them:
```csv
email,name,class,hw1,hw2,quiz1,quiz2,midterm,final,total,grade,comments
```

### 2. Use Clear Column Names
- Use descriptive names: `Homework 1` instead of `HW1`
- Or use short codes: `HW1`, `Q1`, `MT` (they'll be capitalized in emails)

### 3. Include Comments
- Add a `comments` column for personalized feedback
- Or add comments later in the app

### 4. Test First
- Upload a small test file first
- Send a test email to yourself
- Verify the format looks good
- Then upload the full file

---

## 📝 Example Templates

### Template 1: Simple Grading
```csv
email,name,score,grade,comments
student@example.com,John Doe,85,B+,Good work
```

### Template 2: Detailed Breakdown
```csv
email,name,hw1,hw2,hw3,quiz1,quiz2,midterm,final,total,grade
student@example.com,John Doe,90,85,88,92,87,85,89,88.2,A-
```

### Template 3: Multi-Subject
```csv
email,name,math,science,english,history,total,grade,comments
student@example.com,John Doe,85,90,88,92,88.8,A,Excellent all-around
```

---

## ✨ Summary

**The system is designed to accept ANY format you use!**

- Only `email` is required
- Add any columns you want
- They'll all appear in emails
- In the same order as your file
- With comments from CSV or app

**Just upload your file and it works!** 🎉
