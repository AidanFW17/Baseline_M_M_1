# Panduan 30 Replikasi Simulasi M/M/1

## Tujuan

Menjalankan 30 replikasi simulasi dengan random seed berbeda untuk:
- Mendapatkan estimasi KPI yang lebih akurat
- Menganalisis variabilitas hasil simulasi
- Menghitung confidence intervals
- Memvalidasi konsistensi model

## Cara Menjalankan

```bash
cd a3-mm1-simpy
python replications.py
```

## Konfigurasi

- **Jumlah Replikasi**: 30
- **Customer per Replikasi**: 500
- **Base Seed**: 42 (seed untuk replikasi ke-i adalah 42 + i - 1)
- **Arrival Rate (λ)**: 1.0
- **Service Rate (μ)**: 1.2

## Output yang Dihasilkan

### 1. Event Logs (30 file CSV)
- `log_rep_01.csv` sampai `log_rep_30.csv`
- Setiap file berisi event log lengkap untuk satu replikasi
- Format: customer_id, event (arrive/start/depart), time

### 2. KPI Summary (CSV)
- `kpi_summary.csv`
- Tabel dengan 30 baris (satu per replikasi)
- Kolom: Replication, Wq, W, Lq, L

### 3. Complete Data (JSON)
- `all_replications.json`
- Struktur data lengkap termasuk:
  - Metadata (konfigurasi simulasi)
  - Hasil setiap replikasi (seed, KPI)
  - Statistik agregat (mean, std, min, max, median)

### 4. Statistics Summary (TXT)
- `statistics.txt`
- Ringkasan statistik dalam format tabel yang mudah dibaca
- Berisi mean, std, min, max, median untuk setiap KPI

### 5. Analysis Visualizations (PNG)
- `analysis.png`: 12 grafik (4 KPI × 3 jenis plot)
  - Box plot untuk melihat distribusi dan outliers
  - Histogram untuk melihat distribusi frekuensi
  - Line plot untuk melihat trend across replications
  
- `confidence_intervals.png`: 4 grafik confidence intervals
  - 95% CI untuk setiap KPI
  - Scatter plot semua replikasi
  - Mean line dan error bars

## Interpretasi Hasil

### Statistik Agregat

```
        Wq (Avg Wait Time)  W (Avg System Time)  Lq (Avg Queue Length)  L (Avg System Length)
mean              3.911923             4.753872               3.911923               4.753872
std               1.654318             1.677222               1.654318               1.677222
min               1.899289             2.692596               1.899289               2.692596
max               7.782067             8.718262               7.782067               8.718262
median            3.296257             4.138217               3.296257               4.138217
```

### Analisis

1. **Mean vs Theoretical**
   - Mean Wq (3.91) lebih mendekati theoretical (4.17) dibanding single run (7.78)
   - Multiple replications memberikan estimasi lebih akurat

2. **Variabilitas**
   - Standard deviation ~1.65-1.68 menunjukkan variabilitas signifikan
   - Coefficient of variation (CV) = std/mean ≈ 42%
   - Sistem sensitif terhadap random variations

3. **Range**
   - Min-Max range sangat lebar (1.90 - 7.78 untuk Wq)
   - Menunjukkan pentingnya multiple replications
   - Single run bisa sangat misleading

4. **Distribution Shape**
   - Median < Mean mengindikasikan right-skewed distribution
   - Ada beberapa replikasi dengan nilai ekstrem tinggi
   - Typical untuk queueing systems dengan high utilization

5. **Confidence Intervals**
   - 95% CI dapat dihitung: mean ± 1.96 × (std / √30)
   - Untuk Wq: 3.91 ± 0.59 → [3.32, 4.50]
   - Theoretical value (4.17) berada dalam CI

## Kesimpulan

30 replikasi memberikan:
- ✅ Estimasi yang lebih reliable
- ✅ Pemahaman tentang variabilitas sistem
- ✅ Validasi model (hasil mendekati theoretical)
- ✅ Confidence intervals untuk decision making
- ✅ Insight tentang best-case dan worst-case scenarios

## Rekomendasi

Untuk analisis lebih lanjut:
1. Tingkatkan jumlah replikasi (50-100) untuk CI yang lebih sempit
2. Analisis warm-up period untuk menghilangkan transient effects
3. Uji sensitivitas dengan variasi arrival rate dan service rate
4. Bandingkan dengan konfigurasi multi-server (M/M/c)
