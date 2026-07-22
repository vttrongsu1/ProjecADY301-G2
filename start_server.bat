@echo off
chcp 65001 >nul
title Clinical AI - ADY201m Server (Django)
echo =================================================================
echo STARTING CLINICAL AI DIABETES PREDICTION SERVER (DJANGO)
echo =================================================================

set PY_EXE=python
if exist "C:\Users\PC\anaconda3\python.exe" (
    set PY_EXE="C:\Users\PC\anaconda3\python.exe"
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set PY_EXE=py
    )
)

echo Using Python executable: %PY_EXE%

REM Check required Python packages
%PY_EXE% -c "import django, sklearn, pandas, numpy, joblib; print('All packages are ready!')" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [NOTICE] Missing required Python libraries. Auto-installing packages via pip...
    echo.
    %PY_EXE% -m pip install django scikit-learn pandas numpy joblib
)

%PY_EXE% manage.py runserver 0.0.0.0:8000
pause
