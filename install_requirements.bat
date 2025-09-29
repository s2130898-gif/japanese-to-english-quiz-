@echo off
cls
echo ========================================
echo Installing Required Packages...
echo ========================================
echo.
cd /d "%~dp0"

echo Installing Python packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Installation failed
    echo ========================================
    echo.
    echo Please check:
    echo 1. Python is installed
    echo 2. pip is available
    echo 3. Internet connection is active
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next step: Run start_app.bat
echo.
pause