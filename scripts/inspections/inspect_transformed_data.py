"""

scripts/inspections/inspect_transformed_data.py
----------------------------
Script to inspect the transformed (flattened) clinical trial data.

"""

import pandas as pd

df = pd.read_csv("data/processed/clinical_trials.csv")

print(f"Loaded {len(df)} processed trials.")
print("\n--- DataFrame Info ---")
print(df.info())

print("\n--- Sample Rows ---")
print(df.head(5))

# Quick sanity checks
print("\n--- Missing Values Summary ---")
print(df.isna().sum())

print("\n--- Unique Phases ---")
print(df['phase'].unique()[:10])

print("\n--- Unique Statuses ---")
print(df['status'].unique()[:10])
