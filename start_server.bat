@echo off
setlocal enabledelayedexpansion
title Clinical AI - ADY201m Server (Django)
echo =================================================================
echo STARTING CLINICAL AI DIABETES PREDICTION SERVER (DJANGO)
echo =================================================================

set PY_EXE=

REM 1. Thu duong dan Anaconda truoc
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

REM Check required Python packages
!PY_EXE! -c "import django, sklearn, pandas, numpy, joblib; print('All packages are ready!')" 2>nul
if !errorlevel! neq 0 (
    echo [NOTICE] Missing required Python libraries. Auto-installing packages via pip...
    !PY_EXE! -m pip install django scikit-learn pandas numpy joblib
)

REM Tu dong lay dia chi IP cua tung may dang chay (Ke ca khi khong co Internet)
set LOCAL_IP=127.0.0.1
for /f "usebackq tokens=*" %%i in (`!PY_EXE! -c "import socket; ip='127.0.0.1'; try: s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM^); s.connect(('8.8.8.8', 80^)^); ip=s.getsockname()[0^]; s.close(^); except: try: ip=socket.gethostbyname(socket.gethostname(^)^); except: pass; print(ip)" 2^>nul`) do (
    set LOCAL_IP=%%i
)

echo =================================================================
echo 🚀 CLINICAL AI SERVER IS ONLINE!
echo 💻 Local Access: http://127.0.0.1:8000
echo 🌐 LAN/Wi-Fi Access (For other devices): http://!LOCAL_IP!:8000
echo =================================================================
echo.

!PY_EXE! manage.py runserver 0.0.0.0:8000
pause
