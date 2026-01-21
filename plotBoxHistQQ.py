import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats

base_path = "Empower-IQAir"
folders = ["roofTop", "parking", "roofGround"]

# Columns
pm_columns = ["PM1 (ug/m3)", "PM2.5 (ug/m3)", "PM10 (ug/m3)"]
normal_columns = ["Temperature (Celsius)", "Humidity (%)"]

for folder_name in folders:
    csv_path = os.path.join(base_path, f"{folder_name}_temperature_PM_humidity.csv")

    if not os.path.exists(csv_path):
        print(f"Missing file: {csv_path}, skipping")
        continue

    df = pd.read_csv(csv_path)

    plot_data = pd.DataFrame()

    # Keep Temperature & Humidity as-is
    for col in normal_columns:
        if col in df:
            plot_data[col] = df[col]

    # Log(x+1) ONLY for PM values
    for col in pm_columns:
        if col in df:
            plot_data[f"log_{col}"] = np.log(df[col] + 1)

    if plot_data.empty:
        print(f"No valid columns in {folder_name}, skipping")
        continue

    # -----------------------
    # Boxplots
    # -----------------------
    plt.figure(figsize=(12, 6))
    plot_data.boxplot()
    plt.title(f"{folder_name}: Boxplots (PM = log(x+1), Temp & Humidity = original)")
    plt.ylabel("Value")
    plt.xticks(rotation=30, ha="right")
    plt.grid(True, linestyle="--", alpha=0.4)

    boxplot_out = os.path.join(base_path, f"{folder_name}_mixed_boxplot.png")
    plt.tight_layout()
    plt.savefig(boxplot_out, dpi=300)
    plt.close()

    # -----------------------
    # QQ plots
    # -----------------------
    n = len(plot_data.columns)
    cols = 3
    rows = int(np.ceil(n / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(14, 4 * rows))
    axes = axes.flatten()

    for i, col in enumerate(plot_data.columns):
        stats.probplot(plot_data[col].dropna(), dist="norm", plot=axes[i])
        axes[i].set_title(f"QQ plot: {col}")

    # Remove empty panels
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    fig.suptitle(f"{folder_name}: QQ plots (PM log(x+1) only)", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    qq_out = os.path.join(base_path, f"{folder_name}_mixed_qqplots.png")
    plt.savefig(qq_out, dpi=300)
    plt.close()

    # -----------------------
    # Histograms
    # -----------------------
    n = len(plot_data.columns)
    cols = 3
    rows = int(np.ceil(n / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(14, 4 * rows))
    axes = axes.flatten()

    for i, col in enumerate(plot_data.columns):
        axes[i].hist(plot_data[col].dropna(), bins=30)
        axes[i].set_title(f"Histogram: {col}")
        axes[i].set_xlabel("Value")
        axes[i].set_ylabel("Frequency")
        axes[i].grid(True, linestyle="--", alpha=0.4)

    # Remove empty panels
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    fig.suptitle(f"{folder_name}: Histograms (PM log(x+1) only)", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    hist_out = os.path.join(base_path, f"{folder_name}_mixed_histograms.png")
    plt.savefig(hist_out, dpi=300)
    plt.close()

    print(f"Finished {folder_name}")
    print(f"  Boxplot saved to: {boxplot_out}")
    print(f"  QQ plots saved to: {qq_out}")
    print(f"  Histograms saved to: {hist_out}")
