@echo off
REM ===================================================
REM Run KaryaMate Backend (Flask API) in development
REM ===================================================

echo Starting KaryaMate backend...
cd %~dp0
REM Activate virtual environment
call .venv\Scripts\activate

REM Run backend as package
python -m backend.app

pause
