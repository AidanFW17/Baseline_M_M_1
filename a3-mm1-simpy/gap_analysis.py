"""
Script untuk Refleksi & Identifikasi Gap
Membandingkan hasil 30 replikasi dengan nilai teoretis M/M/1
dan mengidentifikasi komponen model yang perlu direvisi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Parameter teoretis
ARRIVAL_RATE = 1.0
SERVICE_RATE = 1.2
RHO = ARRIVAL_RATE / SERVICE_RATE

# Nilai teoretis M/M/1
THEORETICAL = {
    'Wq': RHO / (SERVICE_RATE * (1 - RHO)),
    'W': 1 / (SERVICE_RATE - ARRIVAL_RATE),
    'Lq': (RHO ** 2) / (1 - RHO),
    'L': RHO / (1 - RHO)
}

def calculate_deviation(observed, theoretical):
    """Hitung deviasi absolut dan persentase"""
    abs_deviation = observed - theoretical
    pct_deviation = (abs_deviation / theoretical) * 100
    return abs_deviation, pct_deviation

def perform_hypothesis_test(data, theoretical_value, alpha=0.05):
    """
    Uji hipotesis: H0: μ = theoretical_value vs H1: μ ≠ theoretical_value
    Menggunakan one-sample t-test
    """
    t_statistic, p_value = stats.ttest_1samp(data, theoretical_value)
    reject_h0 = p_value < alpha
    
    return {
        't_statistic': t_statistic,
        'p_value': p_value,
        'reject_h0': reject_h0,
        'conclusion': 'Signifikan berbeda' if reject_h0 else 'Tidak berbeda signifikan'
    }

def analyze_distribution_fit(event_logs_path, num_replications=5):
    """
    Analisis apakah distribusi kedatangan dan layanan sesuai dengan asumsi
    """
    print("\n" + "=" * 80)
    print("ANALISIS DISTRIBUSI (Sample dari 5 Replikasi)")
    print("=" * 80)
    
    interarrival_times = []
    service_times = []
    
    for i in range(1, min(num_replications + 1, 31)):
        df = pd.read_csv(f'{event_logs_path}/log_rep_{i:02d}.csv')
        
        # Hitung interarrival times
        arrivals = df[df['event'] == 'arrive'].sort_values('time')
        if len(arrivals) > 1:
            interarrivals = arrivals['time'].diff().dropna()
            interarrival_times.extend(interarrivals.values)
        
        # Hitung service times
        customer_data = df.pivot(index='customer_id', columns='event', values='time')
        service = customer_data['depart'] - customer_data['start']
        service_times.extend(service.dropna().values)
    
    # Test distribusi eksponensial untuk interarrival times
    print("\n1. INTERARRIVAL TIMES (Seharusnya Exponential dengan rate λ=1.0)")
    print("-" * 80)
    observed_mean_ia = np.mean(interarrival_times)
    theoretical_mean_ia = 1 / ARRIVAL_RATE
    
    print(f"   Theoretical Mean: {theoretical_mean_ia:.4f}")
    print(f"   Observed Mean   : {observed_mean_ia:.4f}")
    print(f"   Deviation       : {abs(observed_mean_ia - theoretical_mean_ia):.4f} ({abs(observed_mean_ia - theoretical_mean_ia)/theoretical_mean_ia*100:.2f}%)")
    
    # Kolmogorov-Smirnov test
    ks_stat_ia, ks_pval_ia = stats.kstest(interarrival_times, 
                                           lambda x: stats.expon.cdf(x, scale=1/ARRIVAL_RATE))
    print(f"   K-S Test p-value: {ks_pval_ia:.4f}")
    if ks_pval_ia > 0.05:
        print(f"   ✓ Distribusi SESUAI dengan Exponential (p > 0.05)")
    else:
        print(f"   ✗ Distribusi TIDAK SESUAI dengan Exponential (p < 0.05)")
        print(f"   → GAP: Distribusi kedatangan perlu direvisi")
    
    # Test distribusi eksponensial untuk service times
    print("\n2. SERVICE TIMES (Seharusnya Exponential dengan rate μ=1.2)")
    print("-" * 80)
    observed_mean_st = np.mean(service_times)
    theoretical_mean_st = 1 / SERVICE_RATE
    
    print(f"   Theoretical Mean: {theoretical_mean_st:.4f}")
    print(f"   Observed Mean   : {observed_mean_st:.4f}")
    print(f"   Deviation       : {abs(observed_mean_st - theoretical_mean_st):.4f} ({abs(observed_mean_st - theoretical_mean_st)/theoretical_mean_st*100:.2f}%)")
    
    ks_stat_st, ks_pval_st = stats.kstest(service_times, 
                                           lambda x: stats.expon.cdf(x, scale=1/SERVICE_RATE))
    print(f"   K-S Test p-value: {ks_pval_st:.4f}")
    if ks_pval_st > 0.05:
        print(f"   ✓ Distribusi SESUAI dengan Exponential (p > 0.05)")
    else:
        print(f"   ✗ Distribusi TIDAK SESUAI dengan Exponential (p < 0.05)")
        print(f"   → GAP: Distribusi layanan perlu direvisi")
    
    return {
        'interarrival': {
            'data': interarrival_times,
            'mean': observed_mean_ia,
            'ks_pvalue': ks_pval_ia,
            'fit_ok': ks_pval_ia > 0.05
        },
        'service': {
            'data': service_times,
            'mean': observed_mean_st,
            'ks_pvalue': ks_pval_st,
            'fit_ok': ks_pval_st > 0.05
        }
    }

def main():
    print("=" * 80)
    print("REFLEKSI & IDENTIFIKASI GAP")
    print("Perbandingan Hasil 30 Replikasi vs Nilai Teoretis M/M/1")
    print("=" * 80)
    
    # Load data
    df_kpi = pd.read_csv('results/replications/kpi_summary.csv')
    df_ci = pd.read_csv('results/replications/confidence_intervals.csv')
    
    metrics_map = {
        'Wq (Avg Wait Time)': 'Wq',
        'W (Avg System Time)': 'W',
        'Lq (Avg Queue Length)': 'Lq',
        'L (Avg System Length)': 'L'
    }
    
    # Analisis deviasi
    print("\n" + "=" * 80)
    print("1. ANALISIS DEVIASI DARI NILAI TEORETIS")
    print("=" * 80)
    
    results = []
    gaps_identified = []
    
    for metric_full, metric_short in metrics_map.items():
        data = df_kpi[metric_full].values
        theoretical = THEORETICAL[metric_short]
        observed_mean = np.mean(data)
        
        abs_dev, pct_dev = calculate_deviation(observed_mean, theoretical)
        
        # Hypothesis test
        h_test = perform_hypothesis_test(data, theoretical)
        
        # CI bounds
        ci_row = df_ci[df_ci['Metric'] == metric_full].iloc[0]
        ci_lower = ci_row['Lower Bound (95% CI)']
        ci_upper = ci_row['Upper Bound (95% CI)']
        theoretical_in_ci = ci_lower <= theoretical <= ci_upper
        
        result = {
            'Metric': metric_short,
            'Theoretical': theoretical,
            'Observed Mean': observed_mean,
            'Abs Deviation': abs_dev,
            'Pct Deviation': pct_dev,
            'CI Lower': ci_lower,
            'CI Upper': ci_upper,
            'Theoretical in CI': theoretical_in_ci,
            't-statistic': h_test['t_statistic'],
            'p-value': h_test['p_value'],
            'Significant Diff': h_test['reject_h0']
        }
        results.append(result)
        
        print(f"\n{metric_full}")
        print("-" * 80)
        print(f"  Theoretical Value      : {theoretical:.4f}")
        print(f"  Observed Mean (n=30)   : {observed_mean:.4f}")
        print(f"  Absolute Deviation     : {abs_dev:+.4f}")
        print(f"  Percentage Deviation   : {pct_dev:+.2f}%")
        print(f"  95% CI                 : [{ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"  Theoretical in CI?     : {'✓ YES' if theoretical_in_ci else '✗ NO'}")
        print(f"  t-statistic            : {h_test['t_statistic']:.4f}")
        print(f"  p-value                : {h_test['p_value']:.4f}")
        print(f"  Conclusion (α=0.05)    : {h_test['conclusion']}")
        
        # Identifikasi gap
        if not theoretical_in_ci or h_test['reject_h0']:
            severity = 'CRITICAL' if abs(pct_dev) > 10 else 'MODERATE' if abs(pct_dev) > 5 else 'MINOR'
            gaps_identified.append({
                'metric': metric_short,
                'severity': severity,
                'deviation_pct': pct_dev,
                'in_ci': theoretical_in_ci,
                'significant': h_test['reject_h0']
            })
    
    # Analisis distribusi
    dist_analysis = analyze_distribution_fit('results/replications')
    
    # Identifikasi komponen yang perlu direvisi
    print("\n" + "=" * 80)
    print("2. IDENTIFIKASI KOMPONEN YANG PERLU DIREVISI")
    print("=" * 80)
    
    issues = []
    
    if len(gaps_identified) > 0:
        print("\nGAP TERIDENTIFIKASI:")
        print("-" * 80)
        for gap in gaps_identified:
            print(f"\n  [{gap['severity']}] {gap['metric']}")
            print(f"    - Deviasi: {gap['deviation_pct']:+.2f}%")
            print(f"    - Theoretical dalam CI: {'Ya' if gap['in_ci'] else 'Tidak'}")
            print(f"    - Signifikan berbeda: {'Ya' if gap['significant'] else 'Tidak'}")
            
            if gap['severity'] in ['CRITICAL', 'MODERATE']:
                issues.append(gap['metric'])
    else:
        print("\n✓ Tidak ada gap signifikan teridentifikasi")
    
    # Rekomendasi spesifik
    print("\n" + "=" * 80)
    print("3. REKOMENDASI REVISI MODEL")
    print("=" * 80)
    
    recommendations = []
    
    # Check distribusi
    if not dist_analysis['interarrival']['fit_ok']:
        recommendations.append({
            'component': 'Distribusi Kedatangan',
            'issue': 'Distribusi interarrival time tidak sesuai dengan Exponential',
            'action': 'Verifikasi random.expovariate(ARRIVAL_RATE) atau gunakan distribusi lain',
            'priority': 'HIGH'
        })
    
    if not dist_analysis['service']['fit_ok']:
        recommendations.append({
            'component': 'Distribusi Layanan',
            'issue': 'Distribusi service time tidak sesuai dengan Exponential',
            'action': 'Verifikasi random.expovariate(SERVICE_RATE) atau gunakan distribusi lain',
            'priority': 'HIGH'
        })
    
    # Check KPI deviations
    if 'Wq' in issues or 'Lq' in issues:
        recommendations.append({
            'component': 'Queue Management',
            'issue': 'Waktu tunggu atau panjang antrian menyimpang dari teoretis',
            'action': 'Periksa logika antrian, warm-up period, atau ukuran simulasi',
            'priority': 'MEDIUM'
        })
    
    if 'W' in issues or 'L' in issues:
        recommendations.append({
            'component': 'System Performance',
            'issue': 'Waktu di sistem atau jumlah customer menyimpang',
            'action': 'Verifikasi logika routing dan perhitungan waktu',
            'priority': 'MEDIUM'
        })
    
    # Jika tidak ada masalah distribusi tapi ada deviasi
    if dist_analysis['interarrival']['fit_ok'] and dist_analysis['service']['fit_ok'] and len(issues) > 0:
        recommendations.append({
            'component': 'Warm-up Period',
            'issue': 'Distribusi benar tapi KPI menyimpang (kemungkinan transient effect)',
            'action': 'Implementasikan warm-up period untuk menghilangkan initial bias',
            'priority': 'MEDIUM'
        })
        
        recommendations.append({
            'component': 'Sample Size',
            'issue': 'Variabilitas tinggi dalam hasil',
            'action': 'Tingkatkan jumlah customer per replikasi atau jumlah replikasi',
            'priority': 'LOW'
        })
    
    if len(recommendations) == 0:
        print("\n✓ MODEL VALID - Tidak ada revisi diperlukan")
        print("\nAlasan:")
        print("  - Semua nilai teoretis berada dalam 95% CI")
        print("  - Tidak ada perbedaan signifikan secara statistik")
        print("  - Distribusi kedatangan dan layanan sesuai dengan asumsi")
    else:
        print("\nKOMPONEN YANG PERLU DIREVISI:")
        print("-" * 80)
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. [{rec['priority']}] {rec['component']}")
            print(f"   Issue : {rec['issue']}")
            print(f"   Action: {rec['action']}")
    
    # Simpan hasil analisis
    df_results = pd.DataFrame(results)
    df_results.to_csv('results/replications/gap_analysis.csv', index=False)
    print(f"\n✓ Hasil analisis disimpan ke 'results/replications/gap_analysis.csv'")
    
    # Simpan laporan lengkap
    with open('results/replications/gap_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("LAPORAN REFLEKSI & IDENTIFIKASI GAP\n")
        f.write("Simulasi Antrian M/M/1 - 30 Replikasi\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("RINGKASAN EKSEKUTIF\n")
        f.write("-" * 80 + "\n")
        if len(recommendations) == 0:
            f.write("✓ Model simulasi VALID dan tidak memerlukan revisi.\n")
            f.write("  Semua KPI berada dalam confidence interval dan distribusi sesuai asumsi.\n")
        else:
            f.write(f"⚠ Teridentifikasi {len(recommendations)} area yang perlu direvisi.\n")
            f.write(f"  {sum(1 for r in recommendations if r['priority'] == 'HIGH')} prioritas HIGH, ")
            f.write(f"{sum(1 for r in recommendations if r['priority'] == 'MEDIUM')} prioritas MEDIUM, ")
            f.write(f"{sum(1 for r in recommendations if r['priority'] == 'LOW')} prioritas LOW.\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("ANALISIS DEVIASI\n")
        f.write("=" * 80 + "\n\n")
        f.write(df_results.to_string(index=False))
        
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("ANALISIS DISTRIBUSI\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Interarrival Times:\n")
        f.write(f"  Mean: {dist_analysis['interarrival']['mean']:.4f} (theoretical: {1/ARRIVAL_RATE:.4f})\n")
        f.write(f"  K-S p-value: {dist_analysis['interarrival']['ks_pvalue']:.4f}\n")
        f.write(f"  Fit: {'✓ OK' if dist_analysis['interarrival']['fit_ok'] else '✗ NOT OK'}\n\n")
        
        f.write(f"Service Times:\n")
        f.write(f"  Mean: {dist_analysis['service']['mean']:.4f} (theoretical: {1/SERVICE_RATE:.4f})\n")
        f.write(f"  K-S p-value: {dist_analysis['service']['ks_pvalue']:.4f}\n")
        f.write(f"  Fit: {'✓ OK' if dist_analysis['service']['fit_ok'] else '✗ NOT OK'}\n")
        
        if len(recommendations) > 0:
            f.write("\n" + "=" * 80 + "\n")
            f.write("REKOMENDASI REVISI\n")
            f.write("=" * 80 + "\n\n")
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. [{rec['priority']}] {rec['component']}\n")
                f.write(f"   Issue : {rec['issue']}\n")
                f.write(f"   Action: {rec['action']}\n\n")
        
        f.write("=" * 80 + "\n")
    
    print(f"✓ Laporan lengkap disimpan ke 'results/replications/gap_analysis_report.txt'")
    
    # Visualisasi
    create_gap_visualization(df_results, dist_analysis)
    
    print("\n" + "=" * 80)
    print("ANALISIS SELESAI!")
    print("=" * 80)

def create_gap_visualization(df_results, dist_analysis):
    """Buat visualisasi gap analysis"""
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Deviation plot
    ax1 = plt.subplot(2, 3, 1)
    metrics = df_results['Metric'].values
    deviations = df_results['Pct Deviation'].values
    colors = ['red' if abs(d) > 5 else 'orange' if abs(d) > 2 else 'green' for d in deviations]
    
    bars = ax1.barh(metrics, deviations, color=colors, alpha=0.7)
    ax1.axvline(0, color='black', linewidth=1)
    ax1.axvline(-5, color='red', linestyle='--', linewidth=0.5, alpha=0.5)
    ax1.axvline(5, color='red', linestyle='--', linewidth=0.5, alpha=0.5)
    ax1.set_xlabel('Deviation from Theoretical (%)')
    ax1.set_title('Percentage Deviation from Theoretical Values', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # 2. Observed vs Theoretical
    ax2 = plt.subplot(2, 3, 2)
    x = np.arange(len(metrics))
    width = 0.35
    
    ax2.bar(x - width/2, df_results['Theoretical'], width, label='Theoretical', color='blue', alpha=0.7)
    ax2.bar(x + width/2, df_results['Observed Mean'], width, label='Observed', color='orange', alpha=0.7)
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics)
    ax2.set_ylabel('Value')
    ax2.set_title('Theoretical vs Observed Values', fontweight='bold')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. p-values
    ax3 = plt.subplot(2, 3, 3)
    pvalues = df_results['p-value'].values
    colors_p = ['red' if p < 0.05 else 'green' for p in pvalues]
    
    ax3.barh(metrics, pvalues, color=colors_p, alpha=0.7)
    ax3.axvline(0.05, color='red', linestyle='--', linewidth=2, label='α = 0.05')
    ax3.set_xlabel('p-value')
    ax3.set_title('Hypothesis Test p-values', fontweight='bold')
    ax3.legend()
    ax3.grid(axis='x', alpha=0.3)
    
    # 4. Interarrival time distribution
    ax4 = plt.subplot(2, 3, 4)
    ia_data = dist_analysis['interarrival']['data']
    ax4.hist(ia_data, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black', label='Observed')
    
    x_range = np.linspace(0, max(ia_data), 100)
    theoretical_pdf = stats.expon.pdf(x_range, scale=1/ARRIVAL_RATE)
    ax4.plot(x_range, theoretical_pdf, 'r-', linewidth=2, label='Theoretical Exp(λ=1.0)')
    
    ax4.set_xlabel('Interarrival Time')
    ax4.set_ylabel('Density')
    ax4.set_title(f'Interarrival Time Distribution\n(K-S p={dist_analysis["interarrival"]["ks_pvalue"]:.4f})', 
                  fontweight='bold')
    ax4.legend()
    ax4.grid(alpha=0.3)
    
    # 5. Service time distribution
    ax5 = plt.subplot(2, 3, 5)
    st_data = dist_analysis['service']['data']
    ax5.hist(st_data, bins=50, density=True, alpha=0.7, color='lightcoral', edgecolor='black', label='Observed')
    
    x_range = np.linspace(0, max(st_data), 100)
    theoretical_pdf = stats.expon.pdf(x_range, scale=1/SERVICE_RATE)
    ax5.plot(x_range, theoretical_pdf, 'r-', linewidth=2, label='Theoretical Exp(μ=1.2)')
    
    ax5.set_xlabel('Service Time')
    ax5.set_ylabel('Density')
    ax5.set_title(f'Service Time Distribution\n(K-S p={dist_analysis["service"]["ks_pvalue"]:.4f})', 
                  fontweight='bold')
    ax5.legend()
    ax5.grid(alpha=0.3)
    
    # 6. CI coverage
    ax6 = plt.subplot(2, 3, 6)
    for i, (_, row) in enumerate(df_results.iterrows()):
        color = 'green' if row['Theoretical in CI'] else 'red'
        ax6.plot([row['CI Lower'], row['CI Upper']], [i, i], 'o-', linewidth=2, markersize=8, color=color)
        ax6.plot(row['Theoretical'], i, '*', markersize=15, color='blue')
        ax6.plot(row['Observed Mean'], i, 's', markersize=8, color='orange')
    
    ax6.set_yticks(range(len(metrics)))
    ax6.set_yticklabels(metrics)
    ax6.set_xlabel('Value')
    ax6.set_title('95% CI Coverage of Theoretical Values', fontweight='bold')
    ax6.legend(['CI Range', 'Theoretical', 'Observed Mean'], loc='best')
    ax6.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/replications/gap_analysis_visualization.png', dpi=300, bbox_inches='tight')
    print(f"✓ Visualisasi disimpan ke 'results/replications/gap_analysis_visualization.png'")
    plt.close()

if __name__ == "__main__":
    main()
