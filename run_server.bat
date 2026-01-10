@echo off
REM Quick start script for Windows
REM Activates virtual environment and runs Django server

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Navigating to Django project directory...
cd mfukoni_web

echo Starting Django development server...
echo.
echo Server will start at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver

pause
