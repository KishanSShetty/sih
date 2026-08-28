@echo off
echo ========================================
echo   Encryption Feature Setup
echo ========================================
echo.

echo Step 1: Installing cryptography package...
echo.
.venv\Scripts\pip.exe install cryptography
echo.

echo Step 2: Creating database tables...
echo (Restart backend to create new tables)
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Restart your backend server
echo 2. Run: python test_encryption.py
echo 3. Check ENCRYPTION_FEATURE.md for full documentation
echo.
pause
