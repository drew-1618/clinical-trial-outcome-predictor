# src/inspections/inspect_transformed_data.py

import pandas as pd

def inspect_transformed_df(path):
    print(f"Loading {path} ...")
    if not path.exists():
        raise FileNotFoundError(f"Missing expected file: {path}")
    df = pd.read_csv(path)

    print(f"Loaded {len(df)} processed trials.")
    print("\n--- DataFrame Info ---")
    print(df.info())

    print("\n--- Sample Rows ---")
    print(df.head(5))

    # Quick sanity checks
    print("\n--- Missing Values Summary ---")
    print(df.isna().sum())

    if "phase" in df.columns:
        print("\n--- Unique Phases ---")
        print(df['phase'].unique()[:10])

    if "status" in df.columns:
        print("\n--- Unique Statuses ---")
        print(df['status'].unique()[:10])
