@echo off
echo ========================================
echo  Python Learning - Local Web Server
echo ========================================
echo.
echo Starting local web server...
echo Open your browser to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d "%~dp0docs"
py -m http.server 8000
