# Simulasi Antrian M/M/1 dengan SimPy

Proyek ini mengimplementasikan simulasi antrian M/M/1 (single server) menggunakan SimPy untuk menganalisis performa sistem antrian.

## Fitur

✅ Model M/M/1 single server dengan SimPy  
✅ Simulasi 500 customer dengan seed konsisten (reproducible)  
✅ Event log lengkap (arrive, start, depart) disimpan ke CSV  
✅ Perhitungan 4 KPI utama: Wq, W, Lq, L  
✅ Visualisasi histogram untuk analisis distribusi  
✅ Sanity check dengan formula teoretis M/M/1  

## Requirements

```bash
pip install simpy pandas matplotlib numpy
```

## Cara Menjalankan

```bash
python mm1_simulation.py
```

## Output

1. **event_log.csv** - Log semua event (arrive, start, depart) untuk setiap customer
2. **simulation_results.png** - Visualisasi histogram Wq dan W
3. **Console output** - Tabel KPI dan perbandingan dengan nilai teoretis

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

## Struktur Kode

```
mm1_simulation.py
├── MM1Queue class       # Model antrian dengan SimPy Resource
├── customer()           # Proses customer (arrive → wait → service → depart)
├── customer_generator() # Generate customer dengan exponential inter-arrival
├── calculate_kpi()      # Hitung 4 KPI dari event log
├── create_visualization() # Buat histogram
└── run_simulation()     # Orchestrate seluruh simulasi
```

## Validasi

Hasil simulasi dibandingkan dengan formula teoretis M/M/1:
- Wq = ρ / (μ(1-ρ))
- W = 1 / (μ-λ)
- Lq = ρ² / (1-ρ)
- L = ρ / (1-ρ)

Hasil simulasi akan mendekati nilai teoretis dengan margin error yang wajar.

## Contoh Output

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

✓ Event log disimpan ke 'event_log.csv'

============================================================
KEY PERFORMANCE INDICATORS (KPI)
============================================================
   Wq (Avg Wait Time)  W (Avg System Time)  Lq (Avg Queue Length)  L (Avg System Length)
             4.123456              5.123456                4.123456                5.123456
============================================================

THEORETICAL VALUES (M/M/1 Formula):
Wq (theory): 4.1667
W (theory): 5.0000
Lq (theory): 4.1667
L (theory): 5.0000
============================================================

✓ Visualisasi disimpan ke 'simulation_results.png'
✓ Simulasi selesai!
```
