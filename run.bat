@echo off
SETLOCAL EnableDelayedExpansion

echo Checking Python installation...
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Removing existing virtual environment...
if exist venv (
    rmdir /s /q venv
)

echo Creating new virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python.exe -m pip install --upgrade pip

echo Installing requirements...
pip install wheel
pip install -r requirements.txt

echo Verifying installations...
python -c "import numpy; print('NumPy version:', numpy.__version__)"
python -c "import sklearn; print('Scikit-learn version:', sklearn.__version__)"

echo Setup complete!
pause