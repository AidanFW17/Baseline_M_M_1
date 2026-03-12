# Script untuk install Python via winget
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalasi Python via winget" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Install Python
Write-Host "Menginstall Python 3.12..." -ForegroundColor Yellow
winget install Python.Python.3.12 --accept-source-agreements --accept-package-agreements

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Python berhasil diinstall!" -ForegroundColor Green
    Write-Host ""
    Write-Host "LANGKAH SELANJUTNYA:" -ForegroundColor Yellow
    Write-Host "1. Tutup terminal ini" -ForegroundColor White
    Write-Host "2. Buka terminal baru" -ForegroundColor White
    Write-Host "3. Jalankan: .\install_and_run.bat" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "[ERROR] Gagal menginstall Python!" -ForegroundColor Red
    Write-Host "Silakan install manual dari: https://www.python.org/downloads/" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Tekan Enter untuk keluar..."
Read-Host
