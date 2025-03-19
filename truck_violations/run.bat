@echo off
echo ===================================
echo Django Application Launch
echo ===================================

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Start the Django server
echo Starting the Django server...
echo The application is accessible at: http://127.0.0.1:8000/
echo To access the admin panel: http://127.0.0.1:8000/admin/
echo.
echo To terminate the application press CTRL+C
echo ===================================

python manage.py runserver