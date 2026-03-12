# Panduan Instalasi Python dan Menjalankan Simulasi

## Masalah yang Terjadi

Windows App Execution Aliases mengalihkan command `python` ke Microsoft Store, sehingga Python yang sebenarnya tidak bisa diakses.

## Solusi Lengkap

### Langkah 1: Nonaktifkan Windows App Execution Aliases

1. Tekan `Windows + I` untuk membuka **Settings**
2. Pilih **Apps**
3. Klik **Advanced app settings** (atau cari "App execution aliases")
4. Scroll ke bawah dan temukan:
   - `python.exe`
   - `python3.exe`
5. **Matikan (OFF)** kedua toggle tersebut

### Langkah 2: Install Python

Pilih salah satu metode:

#### Metode A: Download Manual (RECOMMENDED)

1. Buka browser dan kunjungi: https://www.python.org/downloads/
2. Klik tombol **Download Python 3.x.x**
3. Jalankan installer yang didownload
4. **PENTING:** Centang kotak **"Add Python to PATH"** di bagian bawah
5. Klik **Install Now**
6. Tunggu hingga selesai

#### Metode B: Via winget (Windows Package Manager)

Buka PowerShell sebagai Administrator dan jalankan:

```powershell
winget install Python.Python.3.12 --accept-source-agreements --accept-package-agreements
```

#### Metode C: Via Chocolatey

Jika sudah punya Chocolatey:

```powershell
choco install python -y
```

### Langkah 3: Restart Terminal

**PENTING:** Tutup semua terminal/PowerShell yang terbuka dan buka yang baru.

### Langkah 4: Verifikasi Instalasi

Buka PowerShell baru dan jalankan:

```powershell
python --version
```

Seharusnya muncul: `Python 3.x.x`

### Langkah 5: Jalankan Simulasi

#### Opsi A: Gunakan Batch Script (Otomatis)

Double-click file `install_and_run.bat` atau jalankan di terminal:

```powershell
.\install_and_run.bat
```

Script ini akan:
- Cek Python
- Install dependencies otomatis
- Jalankan simulasi

#### Opsi B: Manual

```powershell
# Install dependencies
python -m pip install simpy pandas matplotlib numpy

# Jalankan simulasi
python mm1_simulation.py
```

## Troubleshooting

### Python masih tidak ditemukan setelah install

1. Pastikan sudah restart terminal
2. Cek PATH environment variable:
   ```powershell
   $env:PATH -split ';' | Select-String Python
   ```
3. Jika tidak ada, tambahkan manual:
   - Cari lokasi Python (biasanya `C:\Users\[Username]\AppData\Local\Programs\Python\Python3xx`)
   - Tambahkan ke System PATH via System Properties

### pip tidak ditemukan

Gunakan:
```powershell
python -m pip install [package]
```

Bukan:
```powershell
pip install [package]
```

### Module tidak ditemukan saat run

Install ulang dependencies:
```powershell
python -m pip install --upgrade simpy pandas matplotlib numpy
```

## Output yang Diharapkan

Setelah berhasil dijalankan, Anda akan mendapatkan:

1. **Console output** dengan tabel KPI
2. **event_log.csv** - Log semua event simulasi
3. **simulation_results.png** - Grafik histogram

## Kontak

Jika masih ada masalah, pastikan:
- Python versi 3.8 atau lebih baru
- Semua dependencies terinstall
- Terminal sudah direstart setelah install Python
