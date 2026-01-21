import pandas as pd
from glob import glob
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
            df["Datetime_start(UTC)"] = pd.to_datetime(df["Datetime_start(UTC)"], errors="coerce")

        dfs.append(df)

    if not dfs:
        print(f"No valid files found in {folder}")
        continue

    combined = pd.concat(dfs, ignore_index=True, sort=False)
    combined = combined.sort_values("Datetime_start(UTC)").reset_index(drop=True)

    csv_out = os.path.join(base_path, f"{folder_name}_temperature_PM_humidity.csv")
    combined.to_csv(csv_out, index=False)

    print(f"Finished {folder_name}")
    print(f"  Combined CSV saved to: {csv_out}")
