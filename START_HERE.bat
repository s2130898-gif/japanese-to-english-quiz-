@echo off
cls
color 0A
echo.
echo     =======================================
echo      Japanese to English Quiz System
echo     =======================================
echo.
echo     [One-Click Setup and Start]
echo.
echo     =======================================
echo.
echo     Processing:
echo     - Check and install packages
echo     - Auto start translation quiz system
echo.
echo     =======================================
echo.
pause

cd /d "%~dp0"

echo Checking Python packages...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo.
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        color 0C
        echo.
        echo ERROR: Failed to install packages
        echo Please run install_requirements.bat manually
        pause
        exit /b 1
    )
    echo Packages installed successfully!
    echo.
)

cls
echo.
echo     =======================================
echo        Starting Translation Quiz System...
echo     =======================================
echo.
echo     Browser will open automatically
echo     URL: http://localhost:8501
echo.
echo     =======================================
echo.
timeout /t 2 /nobreak > nul

streamlit run streamlit_japanese_to_english.py