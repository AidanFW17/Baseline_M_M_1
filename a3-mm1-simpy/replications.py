"""
Script untuk menjalankan 30 replikasi simulasi M/M/1
dengan random seed yang berbeda untuk analisis statistik
"""

import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from metrics import calculate_kpi
import json
from datetime import datetime

# Konfigurasi simulasi
NUM_REPLICATIONS = 30
NUM_CUSTOMERS = 500
ARRIVAL_RATE = 1.0
SERVICE_RATE = 1.2
BASE_SEED = 42

class MM1Queue:
    """Model antrian M/M/1 dengan single server"""
    def __init__(self, env, service_rate):
        self.env = env
        self.server = simpy.Resource(env, capacity=1)
        self.service_rate = service_rate
    
    def service(self, customer_id):
        """Proses layanan dengan exponential service time"""
        service_time = random.expovariate(self.service_rate)
        yield self.env.timeout(service_time)
        return service_time

def customer(env, customer_id, queue, event_log):
    """Proses customer: arrive -> wait -> service -> depart"""
    arrive_time = env.now
    event_log.append({
        'customer_id': customer_id,
        'event': 'arrive',
        'time': arrive_time
    })
    
    with queue.server.request() as request:
        yield request
        
        start_time = env.now
        event_log.append({
            'customer_id': customer_id,
            'event': 'start',
            'time': start_time
        })
        
        yield env.process(queue.service(customer_id))
        
        depart_time = env.now
        event_log.append({
            'customer_id': customer_id,
            'event': 'depart',
            'time': depart_time
        })

def customer_generator(env, queue, arrival_rate, num_customers, event_log):
    """Generate customers dengan exponential inter-arrival time"""
    for i in range(num_customers):
        yield env.timeout(random.expovariate(arrival_rate))
        env.process(customer(env, i, queue, event_log))

def run_single_replication(replication_id, seed):
    """
    Jalankan satu replikasi simulasi
    
    Returns:
    - kpi: Dictionary dengan KPI hasil simulasi
    - event_log: List event log
    """
    # Setup simulasi dengan seed spesifik
    random.seed(seed)
    env = simpy.Environment()
    queue = MM1Queue(env, SERVICE_RATE)
    event_log = []
    
    # Start customer generator
    env.process(customer_generator(env, queue, ARRIVAL_RATE, NUM_CUSTOMERS, event_log))
    
    # Run simulasi
    env.run()
    
    # Convert log ke DataFrame dan hitung KPI
    df_log = pd.DataFrame(event_log)
    kpi, customer_data = calculate_kpi(df_log, ARRIVAL_RATE)
    
    return kpi, df_log

def run_all_replications():
    """Jalankan semua replikasi dan simpan hasilnya"""
    print("=" * 70)
    print("AUTOMASI 30 REPLIKASI SIMULASI M/M/1")
    print("=" * 70)
    print(f"Jumlah Replikasi: {NUM_REPLICATIONS}")
    print(f"Jumlah Customer per Replikasi: {NUM_CUSTOMERS}")
    print(f"Arrival Rate (λ): {ARRIVAL_RATE}")
    print(f"Service Rate (μ): {SERVICE_RATE}")
    print(f"Base Seed: {BASE_SEED}")
    print("=" * 70)
    
    # Struktur data untuk menyimpan hasil
    all_results = {
        'metadata': {
            'num_replications': NUM_REPLICATIONS,
            'num_customers': NUM_CUSTOMERS,
            'arrival_rate': ARRIVAL_RATE,
            'service_rate': SERVICE_RATE,
            'base_seed': BASE_SEED,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'replications': []
    }
    
    # List untuk menyimpan KPI dari semua replikasi
    all_kpi = []
    
    print("\nMenjalankan replikasi...")
    for i in range(NUM_REPLICATIONS):
        seed = BASE_SEED + i
        print(f"  Replikasi {i+1}/{NUM_REPLICATIONS} (seed={seed})...", end=" ")
        
        kpi, event_log = run_single_replication(i+1, seed)
        
        # Simpan hasil replikasi
        replication_result = {
            'replication_id': i + 1,
            'seed': seed,
            'kpi': kpi
        }
        all_results['replications'].append(replication_result)
        all_kpi.append(kpi)
        
        # Simpan event log individual
        df_log = pd.DataFrame(event_log)
        df_log.to_csv(f'results/replications/log_rep_{i+1:02d}.csv', index=False)
        
        print("✓")
    
    # Hitung statistik agregat
    df_kpi = pd.DataFrame(all_kpi)
    
    statistics = {
        'mean': df_kpi.mean().to_dict(),
        'std': df_kpi.std().to_dict(),
        'min': df_kpi.min().to_dict(),
        'max': df_kpi.max().to_dict(),
        'median': df_kpi.median().to_dict()
    }
    
    all_results['statistics'] = statistics
    
    # Simpan hasil ke JSON
    with open('results/replications/all_replications.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n✓ Semua replikasi selesai!")
    print(f"✓ Event logs disimpan ke 'results/replications/log_rep_XX.csv'")
    print(f"✓ Ringkasan disimpan ke 'results/replications/all_replications.json'")
    
    # Simpan ringkasan KPI ke CSV
    df_kpi['Replication'] = range(1, NUM_REPLICATIONS + 1)
    cols = ['Replication'] + [col for col in df_kpi.columns if col != 'Replication']
    df_kpi = df_kpi[cols]
    df_kpi.to_csv('results/replications/kpi_summary.csv', index=False)
    print(f"✓ Ringkasan KPI disimpan ke 'results/replications/kpi_summary.csv'")
    
    # Tampilkan statistik
    print("\n" + "=" * 70)
    print("STATISTIK AGREGAT DARI 30 REPLIKASI")
    print("=" * 70)
    
    stats_df = pd.DataFrame(statistics).T
    print(stats_df.to_string())
    print("=" * 70)
    
    # Simpan statistik ke file txt
    with open('results/replications/statistics.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("STATISTIK AGREGAT DARI 30 REPLIKASI\n")
        f.write("Simulasi Antrian M/M/1\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Jumlah Replikasi: {NUM_REPLICATIONS}\n")
        f.write(f"Jumlah Customer per Replikasi: {NUM_CUSTOMERS}\n")
        f.write(f"Arrival Rate (λ): {ARRIVAL_RATE}\n")
        f.write(f"Service Rate (μ): {SERVICE_RATE}\n\n")
        f.write(stats_df.to_string())
        f.write("\n" + "=" * 70 + "\n")
    
    print(f"\n✓ Statistik disimpan ke 'results/replications/statistics.txt'")
    
    # Buat visualisasi
    create_visualizations(df_kpi, statistics)
    
    return all_results, df_kpi

def create_visualizations(df_kpi, statistics):
    """Buat visualisasi hasil 30 replikasi"""
    
    fig = plt.figure(figsize=(16, 12))
    
    metrics = ['Wq (Avg Wait Time)', 'W (Avg System Time)', 
               'Lq (Avg Queue Length)', 'L (Avg System Length)']
    
    for idx, metric in enumerate(metrics, 1):
        # Box plot
        ax1 = plt.subplot(4, 3, (idx-1)*3 + 1)
        ax1.boxplot([df_kpi[metric]], labels=[''])
        ax1.set_ylabel(metric.split('(')[0].strip())
        ax1.set_title(f'{metric}\nBox Plot', fontsize=10, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Histogram
        ax2 = plt.subplot(4, 3, (idx-1)*3 + 2)
        ax2.hist(df_kpi[metric], bins=15, edgecolor='black', alpha=0.7, color='skyblue')
        ax2.axvline(statistics['mean'][metric], color='red', linestyle='--', 
                    linewidth=2, label=f"Mean={statistics['mean'][metric]:.2f}")
        ax2.set_xlabel('Value')
        ax2.set_ylabel('Frequency')
        ax2.set_title(f'{metric}\nHistogram', fontsize=10, fontweight='bold')
        ax2.legend(fontsize=8)
        ax2.grid(axis='y', alpha=0.3)
        
        # Line plot across replications
        ax3 = plt.subplot(4, 3, (idx-1)*3 + 3)
        ax3.plot(df_kpi['Replication'], df_kpi[metric], marker='o', markersize=3, linewidth=1)
        ax3.axhline(statistics['mean'][metric], color='red', linestyle='--', 
                    linewidth=1, label=f"Mean={statistics['mean'][metric]:.2f}")
        ax3.set_xlabel('Replication')
        ax3.set_ylabel('Value')
        ax3.set_title(f'{metric}\nAcross Replications', fontsize=10, fontweight='bold')
        ax3.legend(fontsize=8)
        ax3.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/replications/analysis.png', dpi=300, bbox_inches='tight')
    print(f"✓ Visualisasi disimpan ke 'results/replications/analysis.png'")
    plt.close()
    
    # Confidence intervals plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, metric in enumerate(metrics):
        mean = statistics['mean'][metric]
        std = statistics['std'][metric]
        ci_95 = 1.96 * std / np.sqrt(NUM_REPLICATIONS)
        
        axes[idx].errorbar([1], [mean], yerr=[ci_95], fmt='o', markersize=10, 
                          capsize=10, capthick=2, color='blue', label='95% CI')
        axes[idx].scatter(df_kpi['Replication'], df_kpi[metric], alpha=0.3, s=30, color='gray')
        axes[idx].axhline(mean, color='red', linestyle='--', linewidth=1, label=f'Mean={mean:.2f}')
        axes[idx].set_xlim(0, NUM_REPLICATIONS + 1)
        axes[idx].set_xlabel('Replication')
        axes[idx].set_ylabel('Value')
        axes[idx].set_title(f'{metric}\n95% Confidence Interval', fontweight='bold')
        axes[idx].legend()
        axes[idx].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/replications/confidence_intervals.png', dpi=300, bbox_inches='tight')
    print(f"✓ Confidence intervals disimpan ke 'results/replications/confidence_intervals.png'")
    plt.close()

if __name__ == "__main__":
    # Buat folder untuk menyimpan hasil replikasi
    import os
    os.makedirs('results/replications', exist_ok=True)
    
    # Jalankan semua replikasi
    all_results, df_kpi = run_all_replications()
    
    print("\n" + "=" * 70)
    print("SELESAI!")
    print("=" * 70)
    print("\nHasil tersimpan di folder 'results/replications/':")
    print("  - log_rep_XX.csv (30 file event log)")
    print("  - kpi_summary.csv (ringkasan KPI semua replikasi)")
    print("  - all_replications.json (data lengkap dalam JSON)")
    print("  - statistics.txt (statistik agregat)")
    print("  - analysis.png (visualisasi box plot, histogram, line plot)")
    print("  - confidence_intervals.png (95% confidence intervals)")
    print("=" * 70)
