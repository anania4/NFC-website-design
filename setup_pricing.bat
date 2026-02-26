@echo off
REM Setup script for dynamic pricing feature (Windows)

echo ==========================================
echo TAP Card Pricing Setup
echo ==========================================
echo.

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo WARNING: Virtual environment not activated
    echo Please activate your virtual environment first:
    echo   venv\Scripts\activate
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

echo Step 1: Running migrations...
python manage.py migrate

if errorlevel 1 (
    echo Migration failed!
    exit /b 1
)

echo Migrations completed
echo.

echo Step 2: Populating initial pricing data...
python manage.py populate_pricing

if errorlevel 1 (
    echo Failed to populate pricing!
    exit /b 1
)

echo Pricing data populated
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Start the server: python manage.py runserver
echo 2. Visit: http://127.0.0.1:8000/card-detail/
echo 3. Manage pricing: http://127.0.0.1:8000/admin/
echo.
echo For more information, see PRICING_SETUP.md
echo.

pause
