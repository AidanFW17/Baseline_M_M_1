@echo off
echo ========================================
echo Instalasi dan Menjalankan Simulasi M/M/1
echo ========================================
echo.

REM Cek apakah Python terinstall
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan!
    echo.
    echo Silakan install Python terlebih dahulu:
    echo 1. Buka https://www.python.org/downloads/
    echo 2. Download Python untuk Windows
    echo 3. Install dan CENTANG "Add Python to PATH"
    echo 4. Restart terminal dan jalankan script ini lagi
    echo.
    pause
    exit /b 1
)

echo [OK] Python ditemukan!
python --version
echo.

echo Menginstall dependencies...
python -m pip install --upgrade pip
python -m pip install simpy pandas matplotlib numpy

if %errorlevel% neq 0 (
    echo [ERROR] Gagal menginstall dependencies!
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies berhasil diinstall!
echo.
echo ========================================
echo Menjalankan Simulasi...
echo ========================================
echo.

python mm1_simulation.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Simulasi gagal dijalankan!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Simulasi selesai!
echo ========================================
pause
