@echo off
cd /d "%~dp0"
echo.
echo ========================================
echo Cell Collective Cookie Extractor
echo ========================================
echo.
echo This will open a browser and extract your session cookie.
echo.
pause
python get_cookie_automatic.py
pause
