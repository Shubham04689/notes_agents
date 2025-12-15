@echo off
REM Setup script for AI Note Generator (Windows)

echo === AI Note Generator Setup ===
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env and add your API keys
)

REM Create output directory
echo.
echo Creating output directory...
if not exist generated_notes mkdir generated_notes

echo.
echo === Setup Complete ===
echo.
echo Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Edit .env file with your API keys
echo 3. Run the application: python main.py
echo.
echo For Ollama users:
echo   - Install Ollama from https://ollama.ai
echo   - Run: ollama serve
echo   - Pull a model: ollama pull llama2
echo.
pause
