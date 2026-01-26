import pandas as pd
import numpy as np
import os
from glob import glob

base_path = "Empower-IQAir"

# These are the files created by your first script
csv_files = glob(os.path.join(base_path, "*_temperature_PM_humidity.csv"))

# Columns we want statistics for
variables = [
    "Temperature (Celsius)",
    "PM1 (ug/m3)",
    "PM2.5 (ug/m3)",
    "PM10 (ug/m3)",
    "Humidity (%)"
]

# Columns to transform by log(x+1)
pm_columns = ["PM1 (ug/m3)", "PM2.5 (ug/m3)", "PM10 (ug/m3)"]

for file in csv_files:
    print(f"Processing: {file}")
    df = pd.read_csv(file)

    stats = []

    # If i want pm to be transformed by log(x+1)
    # for col in pm_columns:
    #     if col in df:
    #         df[col]= np.log(df[col] +1)

    for var in variables:
        if var not in df.columns:
            continue

        series = pd.to_numeric(df[var], errors="coerce")

        stats.append({
            "Variable": var,
            "Mean": series.mean(),
            "Min": series.min(),
            "Max": series.max(),
            "SD": series.std(),
            "DV": series.std()/series.mean()
        })

    if not stats:
        print("  No valid variables found, skipping.")
        continue

    stats_df = pd.DataFrame(stats)

    out_name = os.path.basename(file).replace(".csv", "_discStats.csv")
    out_path = os.path.join(base_path, out_name)

    stats_df.to_csv(out_path, index=False)

    print(f"  Statistics saved to: {out_path}")

print("All files processed.")