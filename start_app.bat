@echo off
cls
color 0A
echo.
echo     =======================================
echo       Japanese to English Quiz System
echo     =======================================
echo.
echo     [Starting Web Interface]
echo.
echo     Browser will open automatically
echo     URL: http://localhost:8501
echo.
echo     =======================================
echo.
pause

cd /d "%~dp0"

echo Starting Japanese to English Translation Quiz...
streamlit run streamlit_japanese_to_english.py

pause