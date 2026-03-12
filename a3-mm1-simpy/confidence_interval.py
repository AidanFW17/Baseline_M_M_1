"""
Script untuk menghitung Confidence Interval 95% dari 30 replikasi
menggunakan t-distribution (karena n=30, bukan distribusi normal)
"""

import pandas as pd
import numpy as np
from scipy import stats

def calculate_confidence_interval(data, confidence=0.95):
    """
    Hitung confidence interval menggunakan t-distribution
    
    Parameters:
    - data: array of values
    - confidence: confidence level (default 0.95 untuk 95%)
    
    Returns:
    - mean, lower_bound, upper_bound, margin_of_error
    """
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)  # Standard error of the mean
    
    # Degrees of freedom
    df = n - 1
    
    # t-critical value untuk 95% CI
    t_critical = stats.t.ppf((1 + confidence) / 2, df)
    
    # Margin of error
    margin_of_error = t_critical * std_err
    
    # Confidence interval
    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error
    
    return mean, lower_bound, upper_bound, margin_of_error, t_critical, std_err

def main():
    print("=" * 80)
    print("KALKULASI CONFIDENCE INTERVAL 95%")
    print("Dari 30 Replikasi Simulasi M/M/1")
    print("=" * 80)
    
    # Load data KPI dari 30 replikasi
    df = pd.read_csv('results/replications/kpi_summary.csv')
    
    print(f"\nJumlah Replikasi (n): {len(df)}")
    print(f"Confidence Level: 95%")
    print(f"Degrees of Freedom (df): {len(df) - 1}")
    
    # Metrics yang akan dihitung
    metrics = [
        'Wq (Avg Wait Time)',
        'W (Avg System Time)',
        'Lq (Avg Queue Length)',
        'L (Avg System Length)'
    ]
    
    results = []
    
    print("\n" + "=" * 80)
    print("HASIL KALKULASI")
    print("=" * 80)
    
    for metric in metrics:
        data = df[metric].values
        mean, lower, upper, moe, t_crit, std_err = calculate_confidence_interval(data)
        
        results.append({
            'Metric': metric,
            'n': len(data),
            'Mean': mean,
            'Std Dev': np.std(data, ddof=1),
            'Std Error': std_err,
            't-critical': t_crit,
            'Margin of Error': moe,
            'Lower Bound (95% CI)': lower,
            'Upper Bound (95% CI)': upper,
            'CI Width': upper - lower
        })
        
        print(f"\n{metric}")
        print("-" * 80)
        print(f"  Sample Size (n)           : {len(data)}")
        print(f"  Mean (x̄)                  : {mean:.6f}")
        print(f"  Standard Deviation (s)    : {np.std(data, ddof=1):.6f}")
        print(f"  Standard Error (SE)       : {std_err:.6f}")
        print(f"  t-critical (α=0.05, df=29): {t_crit:.6f}")
        print(f"  Margin of Error (ME)      : {moe:.6f}")
        print(f"  95% CI                    : [{lower:.6f}, {upper:.6f}]")
        print(f"  CI Width                  : {upper - lower:.6f}")
    
    # Buat tabel ringkasan
    df_results = pd.DataFrame(results)
    
    print("\n" + "=" * 80)
    print("RINGKASAN CONFIDENCE INTERVALS")
    print("=" * 80)
    print("\nFormat Ilmiah:")
    print("-" * 80)
    
    for _, row in df_results.iterrows():
        metric_short = row['Metric'].split('(')[0].strip()
        print(f"{metric_short:25s}: Mean = {row['Mean']:.4f}, 95% CI: [{row['Lower Bound (95% CI)']:.4f}, {row['Upper Bound (95% CI)']:.4f}]")
    
    # Simpan hasil ke file
    df_results.to_csv('results/replications/confidence_intervals.csv', index=False)
    print(f"\n✓ Hasil disimpan ke 'results/replications/confidence_intervals.csv'")
    
    # Simpan laporan lengkap
    with open('results/replications/confidence_interval_report.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("LAPORAN CONFIDENCE INTERVAL 95%\n")
        f.write("Simulasi Antrian M/M/1 - 30 Replikasi\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("METODOLOGI\n")
        f.write("-" * 80 + "\n")
        f.write("Confidence Interval dihitung menggunakan t-distribution karena:\n")
        f.write("  - Sample size (n=30) relatif kecil\n")
        f.write("  - Population standard deviation tidak diketahui\n")
        f.write("  - Menggunakan sample standard deviation sebagai estimator\n\n")
        
        f.write("Formula:\n")
        f.write("  CI = x̄ ± t(α/2, df) × SE\n")
        f.write("  dimana:\n")
        f.write("    x̄  = sample mean\n")
        f.write("    t  = t-critical value (two-tailed, α=0.05, df=29)\n")
        f.write("    SE = standard error = s / √n\n")
        f.write("    s  = sample standard deviation\n")
        f.write("    n  = sample size (30)\n")
        f.write("    df = degrees of freedom = n - 1 = 29\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("HASIL KALKULASI\n")
        f.write("=" * 80 + "\n\n")
        
        for _, row in df_results.iterrows():
            f.write(f"{row['Metric']}\n")
            f.write("-" * 80 + "\n")
            f.write(f"  Sample Size (n)           : {int(row['n'])}\n")
            f.write(f"  Mean (x̄)                  : {row['Mean']:.6f}\n")
            f.write(f"  Standard Deviation (s)    : {row['Std Dev']:.6f}\n")
            f.write(f"  Standard Error (SE)       : {row['Std Error']:.6f}\n")
            f.write(f"  t-critical (α=0.05, df=29): {row['t-critical']:.6f}\n")
            f.write(f"  Margin of Error (ME)      : {row['Margin of Error']:.6f}\n")
            f.write(f"  95% CI                    : [{row['Lower Bound (95% CI)']:.6f}, {row['Upper Bound (95% CI)']:.6f}]\n")
            f.write(f"  CI Width                  : {row['CI Width']:.6f}\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("INTERPRETASI\n")
        f.write("=" * 80 + "\n\n")
        f.write("Confidence Interval 95% berarti:\n")
        f.write("  Jika kita mengulangi eksperimen ini berkali-kali dan menghitung CI\n")
        f.write("  untuk setiap eksperimen, maka 95% dari CI tersebut akan mengandung\n")
        f.write("  true population mean.\n\n")
        
        f.write("Validasi dengan Nilai Teoretis:\n")
        f.write("  Theoretical Wq (M/M/1) = 4.1667\n")
        wq_row = df_results[df_results['Metric'] == 'Wq (Avg Wait Time)'].iloc[0]
        if wq_row['Lower Bound (95% CI)'] <= 4.1667 <= wq_row['Upper Bound (95% CI)']:
            f.write(f"  ✓ Nilai teoretis BERADA DALAM 95% CI [{wq_row['Lower Bound (95% CI)']:.4f}, {wq_row['Upper Bound (95% CI)']:.4f}]\n")
            f.write("  ✓ Model simulasi VALID secara statistik\n")
        else:
            f.write(f"  ✗ Nilai teoretis TIDAK BERADA dalam 95% CI [{wq_row['Lower Bound (95% CI)']:.4f}, {wq_row['Upper Bound (95% CI)']:.4f}]\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("RINGKASAN FORMAT ILMIAH\n")
        f.write("=" * 80 + "\n\n")
        
        for _, row in df_results.iterrows():
            metric_short = row['Metric'].split('(')[0].strip()
            f.write(f"{metric_short:25s}: Mean = {row['Mean']:.4f}, ")
            f.write(f"95% CI: [{row['Lower Bound (95% CI)']:.4f}, {row['Upper Bound (95% CI)']:.4f}]\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    print(f"✓ Laporan lengkap disimpan ke 'results/replications/confidence_interval_report.txt'")
    
    # Buat visualisasi CI
    create_ci_visualization(df_results)
    
    print("\n" + "=" * 80)
    print("SELESAI!")
    print("=" * 80)

def create_ci_visualization(df_results):
    """Buat visualisasi confidence intervals"""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    metrics = df_results['Metric'].values
    means = df_results['Mean'].values
    lower_bounds = df_results['Lower Bound (95% CI)'].values
    upper_bounds = df_results['Upper Bound (95% CI)'].values
    errors = df_results['Margin of Error'].values
    
    # Theoretical values untuk M/M/1
    theoretical = {
        'Wq (Avg Wait Time)': 4.1667,
        'W (Avg System Time)': 5.0000,
        'Lq (Avg Queue Length)': 4.1667,
        'L (Avg System Length)': 5.0000
    }
    
    y_pos = np.arange(len(metrics))
    
    # Plot confidence intervals
    ax.errorbar(means, y_pos, xerr=errors, fmt='o', markersize=10, 
                capsize=10, capthick=2, linewidth=2, color='blue', 
                label='95% CI', elinewidth=2)
    
    # Plot theoretical values
    for i, metric in enumerate(metrics):
        if metric in theoretical:
            ax.axvline(theoretical[metric], color='red', linestyle='--', 
                      linewidth=1, alpha=0.5)
            ax.plot(theoretical[metric], i, 'r*', markersize=15, 
                   label='Theoretical' if i == 0 else '')
    
    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels([m.split('(')[0].strip() for m in metrics])
    ax.set_xlabel('Value', fontsize=12, fontweight='bold')
    ax.set_title('95% Confidence Intervals for KPIs\n(30 Replications)', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='x', alpha=0.3)
    
    # Add CI values as text
    for i, (mean, lower, upper) in enumerate(zip(means, lower_bounds, upper_bounds)):
        ax.text(upper + 0.3, i, f'[{lower:.2f}, {upper:.2f}]', 
               va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('results/replications/ci_visualization.png', dpi=300, bbox_inches='tight')
    print(f"✓ Visualisasi CI disimpan ke 'results/replications/ci_visualization.png'")
    plt.close()

if __name__ == "__main__":
    main()
