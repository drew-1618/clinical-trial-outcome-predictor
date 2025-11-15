# src/pipelines/clean.py

import pandas as pd
import numpy as np
import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer

from src.features.cleaning import (
    clean_phase_column,
    clean_enrollment_column,
    encode_target_status,
    clean_sponsor_column,
    clean_conditions_column,
)

def run_cleaning_pipeline(input_path, output_path):
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

    # Apply feature engineering
    df = clean_sponsor_column(df, top_n=20)
    df = clean_conditions_column(df, max_features=100)

    # Apply final cleaning
    df = df.drop(columns=['nct_id', 'phase', 'enrollment'], errors='ignore')

    # Save cleaned data
    print(f"Saving cleaned data to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("Data cleaning complete.")
