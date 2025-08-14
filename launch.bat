@echo off
REM Seq80x25 Launcher Script for Windows
REM This script launches the retro music sequencer

echo Seq80x25 - Retro Music Sequencer
echo ==================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Check dependencies
echo Checking dependencies...

python -c "import textual" >nul 2>&1
if errorlevel 1 (
    echo Installing textual...
    pip install textual
)

python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Installing pygame...
    pip install pygame
)

python -c "import numpy" >nul 2>&1
if errorlevel 1 (
    echo Installing numpy...
    pip install numpy
)

echo Dependencies OK
echo Launching Seq80x25...

REM Launch the sequencer
python seq80x25.py

echo.
echo Seq80x25 closed
pause
