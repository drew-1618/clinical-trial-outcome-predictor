"""

scripts/audit_trials.py
--------------------------
Quick data quality audit for transformed clinical trial data.
Reports missing values, basic distributions, and potential cleaning targets.

"""

import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/processed/clinical_trials.csv")

def audit_dataframe(df):
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

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing expected file: {DATA_PATH}")

    print(f"Loading {DATA_PATH} ...")
    df = pd.read_csv(DATA_PATH)
    audit_dataframe(df)

if __name__ == "__main__":
    main()
