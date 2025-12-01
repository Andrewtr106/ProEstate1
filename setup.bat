@echo off
echo ========================================
echo    ProEstate Setup Script
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python is installed!
echo.

echo Installing requirements...
pip install flask flask-sqlalchemy flask-wtf wtforms werkzeug

echo.
echo Initializing database...
python init_db.py

echo.
echo Starting website...
echo Website will open at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python run.py

pause