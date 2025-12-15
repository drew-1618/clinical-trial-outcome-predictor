# src/inspections/inspect_interim.py

import pandas as pd
import os


def inspect_interim_df(filepath):
    print(f"Inspecting interim data at {filepath} ...")
    if not os.path.exists(filepath):
        print(f"File not found at {filepath}")
        return
    try:
        df = pd.read_csv(filepath)
        # basic dimensions
        print("\n1. Data Overview:")
        print(f"   - Rows: {df.shape[0]}")
        print(f"   - Columns: {df.shape[1]}")

        # dataframe info
        print("\n2. Column Types:")
        df.info(verbose=False, memory_usage="deep")

        # sample data
        print("\n3. First 5 Rows:")
        print(df.head())

        #  missing values analysis (Only show columns with NaNs)
        print("\n4. Missing Values Summary:")
        missing = df.isna().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            print(missing)
        else:
            print("   (No missing values found)")

        # domain-specific checks
        target_cols = ["phase", "status", "enrollment"]

        for col in target_cols:
            if col in df.columns:
                print(f"\n--- Column Analysis: '{col}' ---")
                unique_vals = df[col].unique()
                print(f"   Unique Count: {len(unique_vals)}")
                print(f"   Sample Values: {unique_vals[:10]}")  # Show first 10
            else:
                print(f"\nWarning: Expected column '{col}' not found.")

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
