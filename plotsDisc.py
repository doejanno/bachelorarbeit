import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.gridspec import GridSpec

base_path = "Empower-IQAir"
folders = ["roofTop", "parking", "roofGround"]

for folder_name in folders:
    csv_path = os.path.join(base_path, f"{folder_name}_temperature_PM_humidity.csv")

    if not os.path.exists(csv_path):
        print(f"Missing file: {csv_path}, skipping")
        continue

    combined = pd.read_csv(csv_path)
    combined["Datetime_start(UTC)"] = pd.to_datetime(combined["Datetime_start(UTC)"], errors="coerce")

    fig = plt.figure(figsize=(14,8))
    gs = GridSpec(2, 6, height_ratios=[2, 1], figure=fig)

    # Large plots (top row)
    ax_temp = fig.add_subplot(gs[0, 0:3])
    ax_hum  = fig.add_subplot(gs[0, 3:6])

    # Small plots (bottom row)
    ax_pm1  = fig.add_subplot(gs[1, 0:2])
    ax_pm25 = fig.add_subplot(gs[1, 2:4])
    ax_pm10 = fig.add_subplot(gs[1, 4:6])

    # ---- Temperature ----
    if "Temperature (Celsius)" in combined:
        ax_temp.plot(combined["Datetime_start(UTC)"], combined["Temperature (Celsius)"])
        ax_temp.set_title("Temperature (°C)")
        ax_temp.set_ylabel("°C")

    # ---- Humidity ----
    if "Humidity (%)" in combined:
        ax_hum.plot(combined["Datetime_start(UTC)"], combined["Humidity (%)"])
        ax_hum.set_title("Humidity (%)")
        ax_hum.set_ylabel("%")

    # ---- PM plots ----
    if "PM1 (ug/m3)" in combined:
        ax_pm1.plot(combined["Datetime_start(UTC)"], combined["PM1 (ug/m3)"])
        ax_pm1.set_title("PM1")

    if "PM2.5 (ug/m3)" in combined:
        ax_pm25.plot(combined["Datetime_start(UTC)"], combined["PM2.5 (ug/m3)"])
        ax_pm25.set_title("PM2.5")

    if "PM10 (ug/m3)" in combined:
        ax_pm10.plot(combined["Datetime_start(UTC)"], combined["PM10 (ug/m3)"])
        ax_pm10.set_title("PM10")

    for ax in [ax_temp, ax_hum, ax_pm1, ax_pm25, ax_pm10]:
        ax.set_xlabel("Datetime")
        ax.grid(True, which="both", linestyle="--", alpha=0.4)
    
    for ax in [ax_pm1, ax_pm25, ax_pm10]:
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)


    fig.suptitle(f"{folder_name}: Temperature, Humidity and PM Levels", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    plot_out = os.path.join(base_path, f"{folder_name}_plot.png")
    plt.savefig(plot_out, dpi=300)
    plt.close()

    print(f"Finished {folder_name}")
    print(f"  Plot saved to: {plot_out}")
