@echo off
echo ===================================
echo AI PM Buddy v2.0 Installation
echo ===================================
echo.

REM Create virtual environment
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to create virtual environment.
    echo Make sure Python 3.11+ is installed and in your PATH.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Some packages failed to install.
    echo You may need to manually install pygraphviz. See win_cmd.txt for instructions.
)

echo.
echo Installation completed!
echo.
echo To run the application:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the app: streamlit run app_v2.py --server.port 8502
echo 3. Open in browser: http://localhost:8502/
echo.
echo Don't forget to update your .env file with your OpenAI API key!
echo.
pause