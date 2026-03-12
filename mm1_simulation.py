import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi simulasi
RANDOM_SEED = 42
NUM_CUSTOMERS = 500
ARRIVAL_RATE = 1.0  # lambda (customers per unit time)
SERVICE_RATE = 1.2  # mu (customers per unit time)

# List untuk menyimpan event log
event_log = []

class MM1Queue:
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

def calculate_kpi(df_log):
    """Hitung 4 KPI utama: Wq, W, Lq, L"""
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
    avg_queue_length = ARRIVAL_RATE * avg_wait_time  # Lq
    avg_system_length = ARRIVAL_RATE * avg_system_time  # L
    
    return {
        'Wq (Avg Wait Time)': avg_wait_time,
        'W (Avg System Time)': avg_system_time,
        'Lq (Avg Queue Length)': avg_queue_length,
        'L (Avg System Length)': avg_system_length
    }, customer_data

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
    df_log.to_csv('event_log.csv', index=False)
    print("\n✓ Event log disimpan ke 'event_log.csv'")
    
    # Hitung KPI
    kpi, customer_data = calculate_kpi(df_log)
    
    # Tampilkan KPI dalam tabel
    print("\n" + "=" * 60)
    print("KEY PERFORMANCE INDICATORS (KPI)")
    print("=" * 60)
    kpi_df = pd.DataFrame([kpi])
    print(kpi_df.to_string(index=False))
    print("=" * 60)
    
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

def create_visualization(customer_data):
    """Buat histogram untuk Wq (waiting time)"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram Wq (Waiting Time in Queue)
    ax1.hist(customer_data['wait_time'], bins=30, edgecolor='black', alpha=0.7, color='skyblue')
    ax1.set_xlabel('Waiting Time (Wq)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Distribution of Waiting Time in Queue', fontsize=14, fontweight='bold')
    ax1.axvline(customer_data['wait_time'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean = {customer_data["wait_time"].mean():.2f}')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Histogram W (Time in System)
    ax2.hist(customer_data['system_time'], bins=30, edgecolor='black', alpha=0.7, color='lightcoral')
    ax2.set_xlabel('Time in System (W)', fontsize=12)
    ax2.set_ylabel('Frequency', fontsize=12)
    ax2.set_title('Distribution of Time in System', fontsize=14, fontweight='bold')
    ax2.axvline(customer_data['system_time'].mean(), color='darkred', linestyle='--', 
                linewidth=2, label=f'Mean = {customer_data["system_time"].mean():.2f}')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('simulation_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Visualisasi disimpan ke 'simulation_results.png'")
    plt.show()

if __name__ == "__main__":
    df_log, kpi, customer_data = run_simulation()
    print("\n✓ Simulasi selesai!")
