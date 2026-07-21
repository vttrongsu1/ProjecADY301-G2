@echo off
setlocal enabledelayedexpansion
title Clinical AI - ADY201m Server (Django)
echo =================================================================
echo STARTING CLINICAL AI DIABETES PREDICTION SERVER (DJANGO)
echo Local access: http://127.0.0.1:8000
echo =================================================================

set PY_EXE=

REM 1. Thu duong dan Anaconda truoc (Uu tien hang dau)
if exist "C:\Users\PC\anaconda3\python.exe" (
    set PY_EXE="C:\Users\PC\anaconda3\python.exe"
)

REM 2. Thu bang Py launcher
if "!PY_EXE!"=="" (
    where py >nul 2>nul
    if !errorlevel! equ 0 set PY_EXE=py
)

REM 3. Thu bang lenh python thuong
if "!PY_EXE!"=="" (
    where python >nul 2>nul
    if !errorlevel! equ 0 set PY_EXE=python
)

REM 4. Fallback ve Anaconda mac dinh
if "!PY_EXE!"=="" set PY_EXE="C:\Users\PC\anaconda3\python.exe"

echo Using Python executable: !PY_EXE!
echo Checking required Python packages (django, scikit-learn, pandas, numpy, joblib)...
!PY_EXE! -c "import django, sklearn, pandas, numpy, joblib; print('All packages are ready!')" 2>nul
if !errorlevel! neq 0 (
    echo.
    echo [NOTICE] Missing required Python libraries. Auto-installing packages via pip...
    echo.
    !PY_EXE! -m pip install django scikit-learn pandas numpy joblib
)

echo.
echo Starting Django Web Server...
!PY_EXE! manage.py runserver 0.0.0.0:8000
pause
