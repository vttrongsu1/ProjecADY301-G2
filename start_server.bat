@echo off
title Clinical AI - ADY201m Server (Django)
echo =================================================================
echo STARTING CLINICAL AI DIABETES PREDICTION SERVER (DJANGO)
echo Local access: http://127.0.0.1:8000
echo =================================================================

set PY_CMD=

REM 1. Kiem tra Python Launcher 'py'
where py >nul 2>nul
if %errorlevel% equ 0 set PY_CMD=py

REM 2. Kiem tra lệnh 'python' trong PATH he thong
if "%PY_CMD%"=="" (
    where python >nul 2>nul
    if %errorlevel% equ 0 set PY_CMD=python
)

REM 3. Kiem tra Anaconda trong thu muc User
if "%PY_CMD%"=="" (
    if exist "%USERPROFILE%\anaconda3\python.exe" set PY_CMD="%USERPROFILE%\anaconda3\python.exe"
)

REM 4. Kiem tra Anaconda o o C:\anaconda3
if "%PY_CMD%"=="" (
    if exist "C:\anaconda3\python.exe" set PY_CMD="C:\anaconda3\python.exe"
)

REM 5. Kiem tra Python chuan trong LocalAppData
if "%PY_CMD%"=="" (
    for /d %%d in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%d\python.exe" set PY_CMD="%%d\python.exe"
    )
)

REM 6. Neu chua tim thay, fallback ve python
if "%PY_CMD%"=="" set PY_CMD=python

echo Using Python executable: %PY_CMD%
echo Checking required Python packages (django, scikit-learn, pandas, numpy, joblib)...
%PY_CMD% -c "import django, sklearn, pandas, numpy, joblib; print('All packages are ready!')" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [NOTICE] Missing required Python libraries. Auto-installing packages via pip...
    echo.
    %PY_CMD% -m pip install django scikit-learn pandas numpy joblib
)

echo.
echo Starting Django Web Server...
%PY_CMD% manage.py runserver 0.0.0.0:8000
pause
