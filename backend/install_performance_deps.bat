@echo off
echo ========================================
echo Installing Performance Testing Dependencies
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Error: Virtual environment not activated
    echo Please run: venv\Scripts\activate
    pause
    exit /b 1
)

echo Installing packages...
pip install requests

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run performance tests with:
echo   python performance_tester.py
echo.
pause