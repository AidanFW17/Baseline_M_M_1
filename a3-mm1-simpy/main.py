"""
Simulasi Antrian M/M/1 dengan SimPy
Main script untuk menjalankan simulasi dan menghasilkan output
"""

import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
from metrics import calculate_kpi, save_kpi_to_file

# Konfigurasi simulasi
RANDOM_SEED = 42
NUM_CUSTOMERS = 500
ARRIVAL_RATE = 1.0  # lambda (customers per unit time)
SERVICE_RATE = 1.2  # mu (customers per unit time)

# List untuk menyimpan event log
event_log = []

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

def customer(env, customer_id, queue):
    """Proses customer: arrive -> wait -> service -> depart"""
    # Arrival
    arrive_time = env.now
    event_log.append({
        'customer_id': customer_id,
        'event': 'arrive',
        'time': arrive_time
    })
    
    # Request server
    with queue.server.request() as request:
        yield request
        
        # Service start
        start_time = env.now
        event_log.append({
            'customer_id': customer_id,
            'event': 'start',
            'time': start_time
        })
        
        # Service process
        yield env.process(queue.service(customer_id))
        
        # Depart
        depart_time = env.now
        event_log.append({
            'customer_id': customer_id,
            'event': 'depart',
            'time': depart_time
        })

def customer_generator(env, queue, arrival_rate, num_customers):
    """Generate customers dengan exponential inter-arrival time"""
    for i in range(num_customers):
        yield env.timeout(random.expovariate(arrival_rate))
        env.process(customer(env, i, queue))

def create_visualization(customer_data):
    """Buat histogram untuk Wq (waiting time)"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Histogram Wq (Waiting Time in Queue)
    ax.hist(customer_data['wait_time'], bins=30, edgecolor='black', alpha=0.7, color='skyblue')
    ax.set_xlabel('Waiting Time (Wq)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Distribution of Waiting Time in Queue (M/M/1)', fontsize=14, fontweight='bold')
    ax.axvline(customer_data['wait_time'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean = {customer_data["wait_time"].mean():.2f}')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/wq_hist.png', dpi=300, bbox_inches='tight')
    print("✓ Visualisasi disimpan ke 'results/wq_hist.png'")
    plt.close()

def run_simulation():
    """Jalankan simulasi lengkap"""
    print("=" * 60)
    print("SIMULASI ANTRIAN M/M/1")
    print("=" * 60)
    print(f"Jumlah Customer: {NUM_CUSTOMERS}")
    print(f"Arrival Rate (λ): {ARRIVAL_RATE}")
    print(f"Service Rate (μ): {SERVICE_RATE}")
    print(f"Utilization (ρ): {ARRIVAL_RATE/SERVICE_RATE:.3f}")
    print(f"Random Seed: {RANDOM_SEED}")
    print("=" * 60)
    
    # Setup simulasi
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    queue = MM1Queue(env, SERVICE_RATE)
    
    # Start customer generator
    env.process(customer_generator(env, queue, ARRIVAL_RATE, NUM_CUSTOMERS))
    
    # Run simulasi
    env.run()
    
    # Convert log ke DataFrame
    df_log = pd.DataFrame(event_log)
    
    # Simpan ke CSV
    df_log.to_csv('results/log.csv', index=False)
    print("\n✓ Event log disimpan ke 'results/log.csv'")
    
    # Hitung KPI
    kpi, customer_data = calculate_kpi(df_log, ARRIVAL_RATE)
    
    # Tampilkan KPI dalam tabel
    print("\n" + "=" * 60)
    print("KEY PERFORMANCE INDICATORS (KPI)")
    print("=" * 60)
    kpi_df = pd.DataFrame([kpi])
    print(kpi_df.to_string(index=False))
    print("=" * 60)
    
    # Simpan KPI ke file
    save_kpi_to_file(kpi, ARRIVAL_RATE, SERVICE_RATE)
    print("\n✓ KPI disimpan ke 'results/kpi.txt'")
    
    # Sanity check dengan teori M/M/1
    rho = ARRIVAL_RATE / SERVICE_RATE
    theoretical_wq = rho / (SERVICE_RATE * (1 - rho))
    theoretical_w = 1 / (SERVICE_RATE - ARRIVAL_RATE)
    theoretical_lq = (rho ** 2) / (1 - rho)
    theoretical_l = rho / (1 - rho)
    
    print("\nTEORITICAL VALUES (M/M/1 Formula):")
    print(f"Wq (theory): {theoretical_wq:.4f}")
    print(f"W (theory): {theoretical_w:.4f}")
    print(f"Lq (theory): {theoretical_lq:.4f}")
    print(f"L (theory): {theoretical_l:.4f}")
    print("=" * 60)
    
    # Buat visualisasi
    create_visualization(customer_data)
    
    return df_log, kpi, customer_data

if __name__ == "__main__":
    df_log, kpi, customer_data = run_simulation()
    print("\n✓ Simulasi selesai!")
    print("\nHasil tersimpan di folder 'results/':")
    print("  - log.csv (event log)")
    print("  - kpi.txt (key performance indicators)")
    print("  - wq_hist.png (histogram waiting time)")
