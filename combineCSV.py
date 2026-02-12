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
            df["Datetime_start(UTC)"] = pd.to_datetime(
                df["Datetime_start(UTC)"], errors="coerce"
            )

        dfs.append(df)

    if not dfs:
        print(f"No valid files found in {folder}")
        continue

    combined = pd.concat(dfs, ignore_index=True, sort=False)
    combined = combined.sort_values("Datetime_start(UTC)").reset_index(drop=True)

    # -----------------------------
    # RESAMPLING PART
    # -----------------------------
    combined = combined.set_index("Datetime_start(UTC)")

    mean_10min = combined.resample("10min").mean()
    mean_30min = combined.resample("30min").mean()

    # Reset index so datetime becomes a column again
    mean_10min = mean_10min.reset_index()
    mean_30min = mean_30min.reset_index()

    # -----------------------------
    # SAVE FILES
    # -----------------------------
    csv_out_raw = os.path.join(base_path, f"{folder_name}_temperature_PM_humidity.csv")
    csv_out_10 = os.path.join(base_path, f"{folder_name}_mean_10min.csv")
    csv_out_30 = os.path.join(base_path, f"{folder_name}_mean_30min.csv")

    combined.reset_index().to_csv(csv_out_raw, index=False)
    mean_10min.to_csv(csv_out_10, index=False)
    mean_30min.to_csv(csv_out_30, index=False)

    print(f"Finished {folder_name}")
    print(f"  Raw CSV saved to: {csv_out_raw}")
    print(f"  10-min mean saved to: {csv_out_10}")
    print(f"  30-min mean saved to: {csv_out_30}")
