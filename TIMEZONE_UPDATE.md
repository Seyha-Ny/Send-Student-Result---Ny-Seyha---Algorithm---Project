# Timezone Update - Asia/Bangkok

## Changes Made

All timestamps in the application have been updated to use **Asia/Bangkok (UTC+7)** timezone instead of UTC.

## Modified Files

### 1. `models.py`
- Added `pytz` import and `BANGKOK_TZ` timezone definition
- Created `get_bangkok_time()` helper function
- Updated all model datetime defaults:
  - `Student.created_at` - now uses Bangkok time
  - `Student.updated_at` - now uses Bangkok time
  - `EmailLog.created_at` - now uses Bangkok time
  - `SharedResult.created_at` - now uses Bangkok time
- Replaced all `datetime.utcnow()` calls with `get_bangkok_time()`

### 2. `email_service.py`
- Added `pytz` import and `BANGKOK_TZ` timezone definition
- Updated email generation timestamp to use Bangkok time
- Updated `email_log.sent_at` to use Bangkok time
- Email footer now shows "(Bangkok Time)" label

### 3. `templates/logs.html`
- Updated JavaScript date formatting to display in Asia/Bangkok timezone
- Changed `toLocaleString()` to include timezone parameter: `'Asia/Bangkok'`

## Impact

### New Records
All new database records will automatically use Bangkok time for timestamps.

### Existing Records
Existing records in the database still have UTC timestamps. They will continue to display as-is unless you run a migration to convert them.

## Display Format

Timestamps are now displayed in the format:
```
MM/DD/YYYY, HH:MM:SS AM/PM
```
Example: `10/28/2025, 11:44:56 AM`

## Dependencies

- `pytz` package (already installed in the environment)

## Testing

To verify the timezone is working correctly:
```bash
python -c "from models import get_bangkok_time; print('Bangkok time:', get_bangkok_time())"
```

Expected output format: `Bangkok time: 2025-10-28 11:44:50.819679+07:00`
