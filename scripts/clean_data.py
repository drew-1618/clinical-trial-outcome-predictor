"""

scripts/clean_data.py
--------------------------
Script to clean clinical trial data
based off scripts/audit_trials.py.

"""

import pandas as pd
import numpy as np
import os

def clean_phase_column(df):
    """Standardize the 'phase' column to consistent categories."""
    # Fill NaNs with unique category to preserve data
    df['phase'] = df['phase'].fillna('NOT_SPECIFIED')

    # Create binary column for each major phase
    major_phases = ['PHASE1', 'PHASE2', 'PHASE3', 'PHASE4']
    for phase in major_phases:
        df[f'is_{phase.lower()}'] = df['phase'].apply(lambda x: 1 if phase in x else 0)
    df['is_phase_not_specified'] = df['phase'].apply(lambda x: 1 if x == 'NOT_SPECIFIED' else 0)

    # Drop original messy phase column
    df.drop(columns=['phase'])

    return df


def clean_enrollment_column(df):
    """
    Imputes missing enrollment values with the median enrollment
    and applies a log transforation to normalize the distribution.
    """
    # Calculate median
    median_enrollment = df['enrollment'].median()
    df['enrollment'] = df['enrollment'].fillna(median_enrollment)

    # Handle zero enrollment since Log(0) is undefined
    df['enrollment_log'] = np.log1p(df['enrollment'])

    # Drop original enrollment column
    df.drop(columns=['enrollment'])

    return df


def encode_target_status(df):
    """
    Encode 'status' column into binary target variable.
    0: TERMINATED (Failure)
    1: COMPLETED (Success)
    """
    # Initialize target column with NaNs
    df['target_outcome'] = np.nan

    # Map TERMINATED to 0
    df.loc[df['status'] == 'TERMINATED', 'target_outcome'] = 0
    
    # Map COMPLETED to 1
    df.loc[df['status'] == 'COMPLETED', 'target_outcome'] = 1
    
    # Drop rows where target is NaN (e.g., 'UNKNOWN', 'RECRUITING', 'WITHDRAWN')
    df = df.dropna(subset=['target_outcome']).copy()
    
    df['target_outcome'] = df['target_outcome'].astype(int)
    
    df = df.drop(columns=['status'])
    return df


def main(input_path, output_path):
    print(f"Loading data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        sys.exit(1)

    print("Starting data cleaning and feature engineering...")

    # Apply cleaning functions
    df = clean_phase_column(df)
    df = clean_enrollment_column(df)
    df = encode_target_status(df)

    # Save cleaned data
    print(f"Saving cleaned data to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Data cleaning complete.")

if __name__ == "__main__":
    INPUT_FILE = 'data/processed/clinical_trials.csv'
    OUTPUT_FILE = 'data/processed/cleaned_trials.csv'

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    main(INPUT_FILE, OUTPUT_FILE)