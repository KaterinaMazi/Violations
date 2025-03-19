@echo off
echo ===================================
echo Django Application Installation
echo ===================================

REM Check if Python exists
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.8+
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate the virtual environment
echo Activating the environment...
call venv\Scripts\activate.bat

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

REM Run migrations
echo Creating the database...
python manage.py makemigrations
echo Applying migrations...
python manage.py migrate

REM Create admin user if it doesn't exist
echo Checking for admin user...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('exists' if User.objects.filter(username='admin').exists() else 'not_exists')" > temp.txt
set /p user_exists=<temp.txt
del temp.txt

if "%user_exists%"=="not_exists" (
    echo Creating admin user...
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')"
    echo Admin user created with:
    echo Username: admin
    echo Password: admin12345
    echo WARNING: Please change the password after first login!
) else (
    echo Admin user already exists.
)


python manage.py migrate
echo Importing data from violations.xlsx file...
python manage.py import_violations


echo.
echo ===================================
echo Installation completed successfully!
echo To start the application, run run.bat
echo ===================================
pause
