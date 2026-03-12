"""
Module untuk menghitung dan menyimpan KPI (Key Performance Indicators)
"""

import pandas as pd

def calculate_kpi(df_log, arrival_rate):
    """
    Hitung 4 KPI utama: Wq, W, Lq, L
    
    Parameters:
    - df_log: DataFrame dengan kolom customer_id, event, time
    - arrival_rate: Lambda (arrival rate)
    
    Returns:
    - kpi: Dictionary dengan 4 KPI
    - customer_data: DataFrame dengan data per customer
    """
    # Pivot data untuk mendapatkan arrive, start, depart per customer
    customer_data = df_log.pivot(index='customer_id', columns='event', values='time')
    
    # Hitung waktu
    customer_data['wait_time'] = customer_data['start'] - customer_data['arrive']  # Wq
    customer_data['service_time'] = customer_data['depart'] - customer_data['start']
    customer_data['system_time'] = customer_data['depart'] - customer_data['arrive']  # W
    
    # KPI 1 & 2: Average waiting time dan system time
    avg_wait_time = customer_data['wait_time'].mean()  # Wq
    avg_system_time = customer_data['system_time'].mean()  # W
    
    # KPI 3 & 4: Average queue length dan system length
    # Menggunakan Little's Law: L = lambda * W, Lq = lambda * Wq
    avg_queue_length = arrival_rate * avg_wait_time  # Lq
    avg_system_length = arrival_rate * avg_system_time  # L
    
    kpi = {
        'Wq (Avg Wait Time)': avg_wait_time,
        'W (Avg System Time)': avg_system_time,
        'Lq (Avg Queue Length)': avg_queue_length,
        'L (Avg System Length)': avg_system_length
    }
    
    return kpi, customer_data

def save_kpi_to_file(kpi, arrival_rate, service_rate):
    """
    Simpan KPI ke file txt dengan format yang rapi
    
    Parameters:
    - kpi: Dictionary dengan KPI
    - arrival_rate: Lambda
    - service_rate: Mu
    """
    with open('results/kpi.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("KEY PERFORMANCE INDICATORS (KPI)\n")
        f.write("Simulasi Antrian M/M/1\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Parameter Simulasi:\n")
        f.write(f"  Arrival Rate (λ): {arrival_rate}\n")
        f.write(f"  Service Rate (μ): {service_rate}\n")
        f.write(f"  Utilization (ρ): {arrival_rate/service_rate:.4f}\n\n")
        
        f.write("Hasil KPI:\n")
        f.write(f"  Wq (Avg Wait Time)      : {kpi['Wq (Avg Wait Time)']:.4f}\n")
        f.write(f"  W  (Avg System Time)    : {kpi['W (Avg System Time)']:.4f}\n")
        f.write(f"  Lq (Avg Queue Length)   : {kpi['Lq (Avg Queue Length)']:.4f}\n")
        f.write(f"  L  (Avg System Length)  : {kpi['L (Avg System Length)']:.4f}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        
        # Nilai teoretis
        rho = arrival_rate / service_rate
        theoretical_wq = rho / (service_rate * (1 - rho))
        theoretical_w = 1 / (service_rate - arrival_rate)
        theoretical_lq = (rho ** 2) / (1 - rho)
        theoretical_l = rho / (1 - rho)
        
        f.write("\nNilai Teoretis (M/M/1 Formula):\n")
        f.write(f"  Wq (theory): {theoretical_wq:.4f}\n")
        f.write(f"  W  (theory): {theoretical_w:.4f}\n")
        f.write(f"  Lq (theory): {theoretical_lq:.4f}\n")
        f.write(f"  L  (theory): {theoretical_l:.4f}\n")
        f.write("=" * 60 + "\n")
