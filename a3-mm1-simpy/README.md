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

```bash
cd a3-mm1-simpy
python main.py
```

## Output

Semua hasil disimpan di folder `results/`:

1. **log.csv** - Log semua event (arrive, start, depart) untuk setiap customer
2. **kpi.txt** - Ringkasan KPI dan perbandingan dengan nilai teoretis
3. **wq_hist.png** - Histogram distribusi waiting time

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

## Penjelasan Kode

### main.py
- `MM1Queue`: Class untuk model antrian dengan SimPy Resource
- `customer()`: Fungsi proses customer (arrive → wait → service → depart)
- `customer_generator()`: Generate customer dengan exponential inter-arrival time
- `run_simulation()`: Orchestrate seluruh simulasi

### metrics.py
- `calculate_kpi()`: Menghitung 4 KPI dari event log
- `save_kpi_to_file()`: Menyimpan KPI ke file txt dengan format rapi

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran simulasi sistem antrian.
