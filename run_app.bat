@echo off
echo =========================================
echo Gemini Vision Color Palette - Launcher
echo =========================================

cd /d "%~dp0"

python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python 3.10+
    pause
    exit /b
)

IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

IF NOT EXIST ".env" (
    echo Please create .env file with GEMINI_API_KEY
    pause
    exit /b
)

streamlit run app.py
pause
