import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_and_compare():
    """Load hasil dari kedua simulasi dan bandingkan"""
    
    print("=" * 70)
    print("PERBANDINGAN SIMULASI M/M/1 vs M/M/2")
    print("=" * 70)
    
    # Load event logs
    try:
        df_mm1 = pd.read_csv('event_log.csv')
        df_mm2 = pd.read_csv('event_log_mm2.csv')
    except FileNotFoundError:
        print("Error: Jalankan mm1_simulation.py dan mm2_simulation.py terlebih dahulu!")
        return
    
    # Calculate KPI untuk M/M/1
    customer_mm1 = df_mm1.pivot(index='customer_id', columns='event', values='time')
    customer_mm1['wait_time'] = customer_mm1['start'] - customer_mm1['arrive']
    customer_mm1['system_time'] = customer_mm1['depart'] - customer_mm1['arrive']
    
    # Calculate KPI untuk M/M/2
    customer_mm2 = df_mm2.pivot(index='customer_id', columns='event', values='time')
    customer_mm2['wait_time'] = customer_mm2['start'] - customer_mm2['arrive']
    customer_mm2['system_time'] = customer_mm2['depart'] - customer_mm2['arrive']
    
    # Buat tabel perbandingan
    comparison = pd.DataFrame({
        'Metric': ['Wq (Avg Wait Time)', 'W (Avg System Time)', 
                   'Lq (Avg Queue Length)', 'L (Avg System Length)'],
        'M/M/1 (1 Server)': [
            customer_mm1['wait_time'].mean(),
            customer_mm1['system_time'].mean(),
            1.0 * customer_mm1['wait_time'].mean(),
            1.0 * customer_mm1['system_time'].mean()
        ],
        'M/M/2 (2 Servers)': [
            customer_mm2['wait_time'].mean(),
            customer_mm2['system_time'].mean(),
            1.0 * customer_mm2['wait_time'].mean(),
            1.0 * customer_mm2['system_time'].mean()
        ]
    })
    
    # Hitung improvement
    comparison['Improvement (%)'] = (
        (comparison['M/M/1 (1 Server)'] - comparison['M/M/2 (2 Servers)']) / 
        comparison['M/M/1 (1 Server)'] * 100
    )
    
    print("\n" + comparison.to_string(index=False))
    print("\n" + "=" * 70)
    
    # Visualisasi perbandingan
    create_comparison_charts(customer_mm1, customer_mm2, comparison)
    
    # Summary
    print("\nKESIMPULAN:")
    print(f"• Penambahan 1 server mengurangi waktu tunggu (Wq) sebesar {comparison.iloc[0]['Improvement (%)']:.1f}%")
    print(f"• Waktu di sistem (W) berkurang sebesar {comparison.iloc[1]['Improvement (%)']:.1f}%")
    print(f"• Panjang antrian (Lq) berkurang sebesar {comparison.iloc[2]['Improvement (%)']:.1f}%")
    print("=" * 70)

def create_comparison_charts(customer_mm1, customer_mm2, comparison):
    """Buat visualisasi perbandingan"""
    
    fig = plt.figure(figsize=(16, 10))
    
    # 1. Bar chart perbandingan KPI
    ax1 = plt.subplot(2, 3, 1)
    metrics = comparison['Metric']
    x = np.arange(len(metrics))
    width = 0.35
    
    ax1.bar(x - width/2, comparison['M/M/1 (1 Server)'], width, label='M/M/1', color='skyblue')
    ax1.bar(x + width/2, comparison['M/M/2 (2 Servers)'], width, label='M/M/2', color='lightgreen')
    ax1.set_xlabel('Metrics')
    ax1.set_ylabel('Value')
    ax1.set_title('KPI Comparison: M/M/1 vs M/M/2', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(['Wq', 'W', 'Lq', 'L'], rotation=0)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. Histogram Wq comparison
    ax2 = plt.subplot(2, 3, 2)
    ax2.hist(customer_mm1['wait_time'], bins=30, alpha=0.6, label='M/M/1', color='skyblue', edgecolor='black')
    ax2.hist(customer_mm2['wait_time'], bins=30, alpha=0.6, label='M/M/2', color='lightgreen', edgecolor='black')
    ax2.set_xlabel('Waiting Time (Wq)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Waiting Time Distribution', fontweight='bold')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Histogram W comparison
    ax3 = plt.subplot(2, 3, 3)
    ax3.hist(customer_mm1['system_time'], bins=30, alpha=0.6, label='M/M/1', color='lightcoral', edgecolor='black')
    ax3.hist(customer_mm2['system_time'], bins=30, alpha=0.6, label='M/M/2', color='lightsalmon', edgecolor='black')
    ax3.set_xlabel('Time in System (W)')
    ax3.set_ylabel('Frequency')
    ax3.set_title('System Time Distribution', fontweight='bold')
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. Box plot Wq
    ax4 = plt.subplot(2, 3, 4)
    ax4.boxplot([customer_mm1['wait_time'], customer_mm2['wait_time']], 
                labels=['M/M/1', 'M/M/2'],
                patch_artist=True,
                boxprops=dict(facecolor='lightblue', alpha=0.7))
    ax4.set_ylabel('Waiting Time (Wq)')
    ax4.set_title('Waiting Time Box Plot', fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    # 5. Box plot W
    ax5 = plt.subplot(2, 3, 5)
    ax5.boxplot([customer_mm1['system_time'], customer_mm2['system_time']], 
                labels=['M/M/1', 'M/M/2'],
                patch_artist=True,
                boxprops=dict(facecolor='lightcoral', alpha=0.7))
    ax5.set_ylabel('Time in System (W)')
    ax5.set_title('System Time Box Plot', fontweight='bold')
    ax5.grid(axis='y', alpha=0.3)
    
    # 6. Improvement percentage
    ax6 = plt.subplot(2, 3, 6)
    improvements = comparison['Improvement (%)']
    colors = ['green' if x > 0 else 'red' for x in improvements]
    ax6.barh(comparison['Metric'], improvements, color=colors, alpha=0.7)
    ax6.set_xlabel('Improvement (%)')
    ax6.set_title('Performance Improvement with 2 Servers', fontweight='bold')
    ax6.axvline(0, color='black', linewidth=0.8)
    ax6.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('comparison_mm1_vs_mm2.png', dpi=300, bbox_inches='tight')
    print("\n✓ Grafik perbandingan disimpan ke 'comparison_mm1_vs_mm2.png'")
    plt.show()

if __name__ == "__main__":
    load_and_compare()
