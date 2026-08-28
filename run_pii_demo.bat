@echo off
echo ========================================
echo   PII Masking Demo - Quick Start
echo ========================================
echo.

echo Step 1: Adding test data with PII...
echo.
python add_test_pii_data.py
echo.

echo Step 2: Exporting database to CSV...
echo.
python export_scans.py
echo.

echo ========================================
echo   Demo Complete!
echo ========================================
echo.
echo The CSV file has been created in this folder.
echo Open it to see PII masking in action!
echo.
echo Look for:
echo   - [EMAIL_REDACTED] where emails were
echo   - [PHONE_REDACTED] where phone numbers were
echo.
pause
