# src/inspections/audit_dataframe

import pandas as pd
from pathlib import Path

def audit_dataframe(path):
    print(f"Loading {path} ...")
    if not path.exists():
        raise FileNotFoundError(f"Missing expected file: {path}")
    df = pd.read_csv(path)

    print("\n=== DATA OVERVIEW ===")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    print("Columns:", list(df.columns))

    print("\n=== MISSING VALUES ===")
    missing = df.isna().sum().sort_values(ascending=False)
    print(missing[missing > 0])

    # Check for duplicates in primary key
    PRIMARY_KEY = "nct_id"
    if PRIMARY_KEY in df.columns:
        if df[PRIMARY_KEY].duplicated().any():
            duplicate_count = df[PRIMARY_KEY].duplicated().sum()
            print(f"\n=== CRITICAL WARNING: PRIMARY KEY DUPLICATES ===")
            print(f"**{duplicate_count}** duplicate entries found for {PRIMARY_KEY}. This needs immediate cleaning.")
        else:
            print(f"\n=== PRIMARY KEY CHECK ===")
            print(f"'{PRIMARY_KEY}' is unique across all {len(df)} records.")


    print("\n=== SAMPLE RECORDS ===")
    print(df.head(3))

    print("\n=== COLUMN TYPES ===")
    print(df.dtypes)

    # Basic stats for numeric columns
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols):
        print("\n=== NUMERIC SUMMARY ===")
        print(df[numeric_cols].describe())

    # Key categorical checks
    for col in ["OverallStatus", "Phase", "StudyType"]:
        if col in df.columns:
            print(f"\n=== {col} value counts ===")
            print(df[col].value_counts(dropna=False).head(10))

    # Date sanity check
    for date_col in ["StartDate", "CompletionDate", "LastUpdatePostDate"]:
        if date_col in df.columns:
            invalid = df[~df[date_col].astype(str).str.match(r"^\d{4}-\d{2}-\d{2}$", na=True)]
            if len(invalid):
                print(f"\n{len(invalid)} records have invalid {date_col} formats.")
