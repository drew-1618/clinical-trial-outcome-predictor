# src/pipelines/data_preparation.py

import pandas as pd
import numpy as np
import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer

from src.features.build_features import (
    clean_phase_column,
    clean_enrollment_column,
    encode_target_status,
    build_sponsor_features,
    build_conditions_feature,
)

def run_preparation_pipeline(input_path, output_path):
    print(f"Loading data from {input_path}...")
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        sys.exit(1)

    df = pd.read_csv(input_path)
    initial_shape = df.shape

    print("Starting data preparation...")

    # Apply cleaning & target encoding
    df = clean_phase_column(df)
    df = clean_enrollment_column(df)
    df = encode_target_status(df)

    # Apply feature engineering
    df = build_sponsor_features(df, top_n=20)
    df = build_conditions_feature(df, max_features=100)

    # Apply final cleaning
    drop_cols = ['nct_id', 'phase', 'enrollment']
    df = df.drop(columns= [c for c in drop_cols if c in df.columns], errors='ignore')

    print("Data preparation complete.")
    print(f"Initial data shape: {initial_shape}, Final data shape: {df.shape}")

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved processed data to {output_path}.")
