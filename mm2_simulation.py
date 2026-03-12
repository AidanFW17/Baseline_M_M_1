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
NUM_SERVERS = 2     # Jumlah server

# List untuk menyimpan event log
event_log = []

class MM2Queue:
    def __init__(self, env, service_rate, num_servers):
        self.env = env
        self.server = simpy.Resource(env, capacity=num_servers)
        self.service_rate = service_rate
        self.num_servers = num_servers
    
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

def calculate_mm2_theoretical():
    """Hitung nilai teoretis untuk M/M/2"""
    import math
    c = NUM_SERVERS
    lam = ARRIVAL_RATE
    mu = SERVICE_RATE
    rho = lam / (c * mu)  # Utilization per server
    
    # Probability of zero customers in system (P0)
    sum_term = sum([(c * rho) ** n / math.factorial(n) for n in range(c)])
    last_term = (c * rho) ** c / (math.factorial(c) * (1 - rho))
    P0 = 1 / (sum_term + last_term)
    
    # Average number in queue (Lq)
    Lq = (P0 * (lam / mu) ** c * rho) / (math.factorial(c) * (1 - rho) ** 2)
    
    # Average waiting time in queue (Wq)
    Wq = Lq / lam
    
    # Average time in system (W)
    W = Wq + (1 / mu)
    
    # Average number in system (L)
    L = lam * W
    
    return {
        'Wq': Wq,
        'W': W,
        'Lq': Lq,
        'L': L,
        'rho': rho,
        'P0': P0
    }

def run_simulation():
    """Jalankan simulasi lengkap"""
    print("=" * 60)
    print("SIMULASI ANTRIAN M/M/2 (2 SERVER)")
    print("=" * 60)
    print(f"Jumlah Customer: {NUM_CUSTOMERS}")
    print(f"Jumlah Server: {NUM_SERVERS}")
    print(f"Arrival Rate (λ): {ARRIVAL_RATE}")
    print(f"Service Rate (μ): {SERVICE_RATE}")
    print(f"Utilization per server (ρ): {ARRIVAL_RATE/(NUM_SERVERS*SERVICE_RATE):.3f}")
    print(f"Random Seed: {RANDOM_SEED}")
    print("=" * 60)
    
    # Setup simulasi
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    queue = MM2Queue(env, SERVICE_RATE, NUM_SERVERS)
    
    # Start customer generator
    env.process(customer_generator(env, queue, ARRIVAL_RATE, NUM_CUSTOMERS))
    
    # Run simulasi
    env.run()
    
    # Convert log ke DataFrame
    df_log = pd.DataFrame(event_log)
    
    # Simpan ke CSV
    df_log.to_csv('event_log_mm2.csv', index=False)
    print("\n✓ Event log disimpan ke 'event_log_mm2.csv'")
    
    # Hitung KPI
    kpi, customer_data = calculate_kpi(df_log)
    
    # Tampilkan KPI dalam tabel
    print("\n" + "=" * 60)
    print("KEY PERFORMANCE INDICATORS (KPI)")
    print("=" * 60)
    kpi_df = pd.DataFrame([kpi])
    print(kpi_df.to_string(index=False))
    print("=" * 60)
    
    # Hitung dan tampilkan nilai teoretis
    theoretical = calculate_mm2_theoretical()
    print("\nTEORITICAL VALUES (M/M/2 Formula):")
    print(f"Wq (theory): {theoretical['Wq']:.4f}")
    print(f"W (theory): {theoretical['W']:.4f}")
    print(f"Lq (theory): {theoretical['Lq']:.4f}")
    print(f"L (theory): {theoretical['L']:.4f}")
    print(f"P0 (probability empty): {theoretical['P0']:.4f}")
    print("=" * 60)
    
    # Buat visualisasi
    create_visualization(customer_data)
    
    return df_log, kpi, customer_data

def create_visualization(customer_data):
    """Buat histogram untuk Wq (waiting time)"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram Wq (Waiting Time in Queue)
    ax1.hist(customer_data['wait_time'], bins=30, edgecolor='black', alpha=0.7, color='lightgreen')
    ax1.set_xlabel('Waiting Time (Wq)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('M/M/2: Distribution of Waiting Time in Queue', fontsize=14, fontweight='bold')
    ax1.axvline(customer_data['wait_time'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean = {customer_data["wait_time"].mean():.2f}')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Histogram W (Time in System)
    ax2.hist(customer_data['system_time'], bins=30, edgecolor='black', alpha=0.7, color='lightsalmon')
    ax2.set_xlabel('Time in System (W)', fontsize=12)
    ax2.set_ylabel('Frequency', fontsize=12)
    ax2.set_title('M/M/2: Distribution of Time in System', fontsize=14, fontweight='bold')
    ax2.axvline(customer_data['system_time'].mean(), color='darkred', linestyle='--', 
                linewidth=2, label=f'Mean = {customer_data["system_time"].mean():.2f}')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('simulation_results_mm2.png', dpi=300, bbox_inches='tight')
    print("\n✓ Visualisasi disimpan ke 'simulation_results_mm2.png'")
    plt.show()

if __name__ == "__main__":
    df_log, kpi, customer_data = run_simulation()
    print("\n✓ Simulasi M/M/2 selesai!")
