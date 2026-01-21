import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import os

base_path = "Empower-IQAir"
folders = ["roofTop", "parking", "roofGround"]

columns_to_keep = [
    "Datetime_start(UTC)",
    "Temperature (Celsius)",
    "PM2.5 (ug/m3)",
    "PM10 (ug/m3)",
    "PM1 (ug/m3)",
    "Humidity (%)"
]

for folder_name in folders:
    folder = os.path.join(base_path, folder_name)
    files = glob(f"{folder}/*.csv")

    dfs = []

    for f in files:
        df = pd.read_csv(f, engine="python")

        # Normalize datetime column name
        if "Datetime_start" in df.columns and "Datetime_start(UTC)" not in df.columns:
            df = df.rename(columns={"Datetime_start": "Datetime_start(UTC)"})

        existing_cols = [c for c in columns_to_keep if c in df.columns]
        if not existing_cols:
            print(f"No columns to keep in {f}, skipping")
            continue

        df = df[existing_cols]

        if "Datetime_start(UTC)" in df.columns:
            df["Datetime_start(UTC)"] = pd.to_datetime(df["Datetime_start(UTC)"], errors='coerce')

        dfs.append(df)

    if not dfs:
        print(f"No valid files found in {folder}")
        continue

    combined = pd.concat(dfs, ignore_index=True, sort=False)
    combined = combined.sort_values("Datetime_start(UTC)").reset_index(drop=True)

    # Save combined CSV
    csv_out = os.path.join(base_path, f"{folder_name}_temperature_PM_humidity.csv")
    combined.to_csv(csv_out, index=False)

    # Plot
    plt.figure(figsize=(12,5))
    if "Temperature (Celsius)" in combined:
        plt.plot(combined["Datetime_start(UTC)"], combined["Temperature (Celsius)"], label="Temp (°C)")
    if "PM1 (ug/m3)" in combined:
        plt.plot(combined["Datetime_start(UTC)"], combined["PM1 (ug/m3)"], label="PM1")
    if "PM2.5 (ug/m3)" in combined:
        plt.plot(combined["Datetime_start(UTC)"], combined["PM2.5 (ug/m3)"], label="PM2.5")
    if "PM10 (ug/m3)" in combined:
        plt.plot(combined["Datetime_start(UTC)"], combined["PM10 (ug/m3)"], label="PM10")
    if "Humidity (%)" in combined:
        plt.plot(combined["Datetime_start(UTC)"], combined["Humidity (%)"], label="Humidity (%)")

    plt.xlabel("Datetime")
    plt.ylabel("Values")
    plt.title(f"{folder_name}: Temperature, PM, Humidity")
    plt.legend()
    plt.tight_layout()

    # Save plot
    plot_out = os.path.join(base_path, f"{folder_name}_plot.png")
    plt.savefig(plot_out, dpi=300)
    plt.close()

    print(f"Finished {folder_name}")
    print(f"  CSV saved to: {csv_out}")
    print(f"  Plot saved to: {plot_out}")