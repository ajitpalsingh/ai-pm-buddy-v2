@echo off
echo ===================================
echo AI PM Buddy v2.0
echo ===================================
echo.

REM Activate virtual environment
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to activate virtual environment.
    echo Make sure you've run install.bat first.
    pause
    exit /b 1
)

REM Run the application
echo Starting AI PM Buddy v2.0...
echo Application will be available at: http://localhost:8502/
echo.
streamlit run app_v2.py --server.port 8502