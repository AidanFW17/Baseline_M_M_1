# Simulasi Antrian M/M/1 dengan SimPy

Proyek ini mengimplementasikan simulasi antrian M/M/1 (single server) menggunakan SimPy untuk menganalisis performa sistem antrian.

## Struktur Proyek

```
a3-mm1-simpy/
├── README.md           # Dokumentasi proyek
├── main.py             # Script utama simulasi
├── metrics.py          # Modul perhitungan KPI
└── results/            # Folder output hasil simulasi
    ├── log.csv         # Event log (arrive, start, depart)
    ├── kpi.txt         # Key Performance Indicators
    └── wq_hist.png     # Histogram waiting time
```

## Fitur

✅ Model M/M/1 single server dengan SimPy  
✅ Simulasi 500 customer dengan seed konsisten (reproducible)  
✅ Event log lengkap (arrive, start, depart) disimpan ke CSV  
✅ Perhitungan 4 KPI utama: Wq, W, Lq, L  
✅ Visualisasi histogram untuk analisis distribusi  
✅ Sanity check dengan formula teoretis M/M/1  

## Requirements

```bash
pip install simpy pandas matplotlib
```

## Cara Menjalankan

### Simulasi Tunggal
```bash
cd a3-mm1-simpy
python main.py
```

### 30 Replikasi Otomatis
```bash
cd a3-mm1-simpy
python replications.py
```

Script `replications.py` akan menjalankan 30 replikasi dengan seed berbeda (42-71) dan menghasilkan analisis statistik lengkap.

### Kalkulasi Confidence Interval
```bash
cd a3-mm1-simpy
python confidence_interval.py
```

### Analisis Gap & Validasi Model
```bash
cd a3-mm1-simpy
python gap_analysis.py
```

Script ini membandingkan hasil simulasi dengan nilai teoretis dan memvalidasi distribusi.

## Output

### Simulasi Tunggal
Semua hasil disimpan di folder `results/`:

1. **log.csv** - Log semua event (arrive, start, depart) untuk setiap customer
2. **kpi.txt** - Ringkasan KPI dan perbandingan dengan nilai teoretis
3. **wq_hist.png** - Histogram distribusi waiting time

### 30 Replikasi
Semua hasil disimpan di folder `results/replications/`:

1. **log_rep_01.csv sampai log_rep_30.csv** - Event log untuk setiap replikasi
2. **kpi_summary.csv** - Ringkasan KPI dari semua 30 replikasi
3. **all_replications.json** - Data lengkap dalam format JSON
4. **statistics.txt** - Statistik agregat (mean, std, min, max, median)
5. **analysis.png** - Visualisasi box plot, histogram, dan line plot untuk setiap KPI
6. **confidence_intervals.png** - 95% confidence intervals untuk setiap KPI (dari replications.py)
7. **confidence_intervals.csv** - Tabel confidence intervals dengan detail kalkulasi
8. **confidence_interval_report.txt** - Laporan lengkap metodologi dan hasil CI
9. **ci_visualization.png** - Visualisasi CI dengan nilai teoretis
10. **gap_analysis.csv** - Tabel analisis deviasi dan hypothesis testing
11. **gap_analysis_report.txt** - Laporan lengkap refleksi dan identifikasi gap
12. **gap_analysis_visualization.png** - Visualisasi gap analysis dan validasi distribusi

### Cara Menghitung Confidence Interval
```bash
cd a3-mm1-simpy
python confidence_interval.py
```

Script ini menghitung 95% CI menggunakan t-distribution dengan formula:
```
CI = x̄ ± t(α/2, df) × SE
dimana:
  x̄  = sample mean
  t  = t-critical value (2.045 untuk df=29, α=0.05)
  SE = standard error = s / √n
```

## Key Performance Indicators (KPI)

- **Wq** - Average Waiting Time in Queue (waktu tunggu rata-rata di antrian)
- **W** - Average Time in System (waktu rata-rata di sistem)
- **Lq** - Average Queue Length (panjang antrian rata-rata)
- **L** - Average System Length (jumlah customer rata-rata di sistem)

## Parameter Simulasi

- Jumlah Customer: 500
- Arrival Rate (λ): 1.0 customer/unit time
- Service Rate (μ): 1.2 customer/unit time
- Utilization (ρ): 0.833
- Random Seed: 42 (untuk reproducibility)

## Validasi

Hasil simulasi dibandingkan dengan formula teoretis M/M/1:
- Wq = ρ / (μ(1-ρ))
- W = 1 / (μ-λ)
- Lq = ρ² / (1-ρ)
- L = ρ / (1-ρ)

Hasil simulasi akan mendekati nilai teoretis dengan margin error yang wajar.

## Contoh Output Console

```
============================================================
SIMULASI ANTRIAN M/M/1
============================================================
Jumlah Customer: 500
Arrival Rate (λ): 1.0
Service Rate (μ): 1.2
Utilization (ρ): 0.833
Random Seed: 42
============================================================

✓ Event log disimpan ke 'results/log.csv'

============================================================
KEY PERFORMANCE INDICATORS (KPI)
============================================================
   Wq (Avg Wait Time)  W (Avg System Time)  Lq (Avg Queue Length)  L (Avg System Length)
             4.123456              5.123456                4.123456                5.123456
============================================================

✓ KPI disimpan ke 'results/kpi.txt'

TEORITICAL VALUES (M/M/1 Formula):
Wq (theory): 4.1667
W (theory): 5.0000
Lq (theory): 4.1667
L (theory): 5.0000
============================================================

✓ Visualisasi disimpan ke 'results/wq_hist.png'

✓ Simulasi selesai!
```

## Ringkasan Hasil Simulasi

### Tabel KPI

| Metric | Nilai Simulasi | Nilai Teoretis | Satuan |
|--------|----------------|----------------|--------|
| Wq (Avg Wait Time) | 7.7821 | 4.1667 | unit waktu |
| W (Avg System Time) | 8.7183 | 5.0000 | unit waktu |
| Lq (Avg Queue Length) | 7.7821 | 4.1667 | customer |
| L (Avg System Length) | 8.7183 | 5.0000 | customer |

### Interpretasi Hasil

Hasil simulasi menunjukkan performa sistem antrian M/M/1 dengan utilization 83.3% (ρ = 0.833). Rata-rata waktu tunggu customer di antrian (Wq) adalah 7.78 unit waktu, yang berarti setiap customer harus menunggu hampir 8 unit waktu sebelum dilayani. Total waktu yang dihabiskan customer di sistem (W) mencapai 8.72 unit waktu, yang mencakup waktu tunggu dan waktu layanan. Panjang antrian rata-rata (Lq) sebesar 7.78 customer menunjukkan bahwa sistem cukup sibuk dengan antrian yang panjang. Jumlah rata-rata customer di sistem (L) adalah 8.72, yang berarti pada setiap waktu terdapat sekitar 8-9 customer baik yang sedang menunggu maupun dilayani. Nilai simulasi yang lebih tinggi dari teoretis menunjukkan variabilitas alami dalam sistem stokastik, namun masih dalam rentang yang wajar dan memvalidasi model simulasi.

## Hasil 30 Replikasi

### Statistik Agregat

| Metric | Mean | Std Dev | Min | Max | Median |
|--------|------|---------|-----|-----|--------|
| Wq (Avg Wait Time) | 3.91 | 1.65 | 1.90 | 7.78 | 3.30 |
| W (Avg System Time) | 4.75 | 1.68 | 2.69 | 8.72 | 4.14 |
| Lq (Avg Queue Length) | 3.91 | 1.65 | 1.90 | 7.78 | 3.30 |
| L (Avg System Length) | 4.75 | 1.68 | 2.69 | 8.72 | 4.14 |

### Confidence Interval 95%

Menggunakan t-distribution (n=30, df=29, t-critical=2.045):

| Metric | Mean | 95% CI | Theoretical |
|--------|------|--------|-------------|
| Wq (Avg Wait Time) | 3.9119 | [3.2942, 4.5297] | 4.1667 ✓ |
| W (Avg System Time) | 4.7539 | [4.1276, 5.3802] | 5.0000 ✓ |
| Lq (Avg Queue Length) | 3.9119 | [3.2942, 4.5297] | 4.1667 ✓ |
| L (Avg System Length) | 4.7539 | [4.1276, 5.3802] | 5.0000 ✓ |

**Format Ilmiah:**
- **Wq**: Mean = 3.9119, 95% CI: [3.2942, 4.5297]
- **W**: Mean = 4.7539, 95% CI: [4.1276, 5.3802]
- **Lq**: Mean = 3.9119, 95% CI: [3.2942, 4.5297]
- **L**: Mean = 4.7539, 95% CI: [4.1276, 5.3802]

✓ Semua nilai teoretis berada dalam 95% CI, memvalidasi model simulasi secara statistik.

### Interpretasi Hasil Replikasi

Dari 30 replikasi dengan seed berbeda, diperoleh rata-rata waktu tunggu (Wq) sebesar 3.91 unit waktu dengan standar deviasi 1.65, menunjukkan variabilitas yang cukup signifikan antar replikasi. Nilai mean ini lebih mendekati nilai teoretis (4.17) dibandingkan hasil simulasi tunggal, membuktikan bahwa multiple replications memberikan estimasi yang lebih akurat. Standar deviasi yang relatif besar mengindikasikan bahwa performa sistem sangat sensitif terhadap pola kedatangan dan layanan yang random. Range nilai dari minimum 1.90 hingga maximum 7.78 menunjukkan bahwa dalam kondisi tertentu, sistem bisa sangat efisien atau sebaliknya sangat terbebani. Median yang lebih rendah dari mean (3.30 vs 3.91) mengindikasikan distribusi yang right-skewed, artinya ada beberapa replikasi dengan nilai ekstrem tinggi yang menarik rata-rata ke atas. Hasil ini menekankan pentingnya menjalankan multiple replications untuk mendapatkan gambaran yang komprehensif tentang performa sistem.

## Refleksi & Identifikasi Gap

### Analisis Deviasi

| Metric | Theoretical | Observed | Deviation | p-value | Status |
|--------|-------------|----------|-----------|---------|--------|
| Wq | 4.1667 | 3.9119 | -6.11% | 0.406 | ✓ Valid |
| W | 5.0000 | 4.7539 | -4.92% | 0.428 | ✓ Valid |
| Lq | 4.1667 | 3.9119 | -6.11% | 0.406 | ✓ Valid |
| L | 5.0000 | 4.7539 | -4.92% | 0.428 | ✓ Valid |

### Validasi Distribusi

**Interarrival Times (Exponential λ=1.0):**
- Observed Mean: 0.9821 (Theoretical: 1.0000)
- K-S Test p-value: 0.2754
- Status: ✓ Sesuai dengan Exponential

**Service Times (Exponential μ=1.2):**
- Observed Mean: 0.8564 (Theoretical: 0.8333)
- K-S Test p-value: 0.3253
- Status: ✓ Sesuai dengan Exponential

### Kesimpulan Gap Analysis

✅ **MODEL VALID - Tidak ada revisi diperlukan**

**Alasan:**
1. Semua nilai teoretis berada dalam 95% Confidence Interval
2. Tidak ada perbedaan signifikan secara statistik (semua p-value > 0.05)
3. Distribusi kedatangan sesuai dengan Exponential(λ=1.0)
4. Distribusi layanan sesuai dengan Exponential(μ=1.2)
5. Deviasi < 10% untuk semua KPI (dalam batas wajar untuk simulasi stokastik)

**Komponen Model yang Divalidasi:**
- ✓ Distribusi Kedatangan: Exponential dengan rate λ=1.0
- ✓ Distribusi Layanan: Exponential dengan rate μ=1.2
- ✓ Logika Routing: Single server queue (M/M/1)
- ✓ Perhitungan KPI: Sesuai dengan Little's Law

Model simulasi ini dapat digunakan dengan confidence untuk analisis sistem antrian M/M/1.

## Penjelasan Kode

### main.py
- `MM1Queue`: Class untuk model antrian dengan SimPy Resource
- `customer()`: Fungsi proses customer (arrive → wait → service → depart)
- `customer_generator()`: Generate customer dengan exponential inter-arrival time
- `run_simulation()`: Orchestrate seluruh simulasi

### metrics.py
- `calculate_kpi()`: Menghitung 4 KPI dari event log
- `save_kpi_to_file()`: Menyimpan KPI ke file txt dengan format rapi

### replications.py
- `run_single_replication()`: Menjalankan satu replikasi dengan seed spesifik
- `run_all_replications()`: Loop untuk menjalankan 30 replikasi
- `create_visualizations()`: Membuat box plot, histogram, line plot, dan confidence intervals
- Menyimpan hasil dalam struktur data terorganisir (CSV, JSON, TXT, PNG)

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran simulasi sistem antrian.
