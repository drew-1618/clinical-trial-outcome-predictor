# src/pipelines/transform.py

import json
import pandas as pd
from src.utils.flattening import flatten_study

RAW_PATH = "data/raw/clinical_trials.json"
OUT_PATH = "data/processed/clinical_trials.csv"

def transform_trials():
    with open(RAW_PATH, "r") as f:
        data = json.load(f)
    
    # Handle both list and dict formats
    if isinstance(data, list):
        studies = data
    elif isinstance(data, dict) and "studies" in data:
        studies = data["studies"]
    else:
        raise ValueError("Unexpected JSON format — could not find studies list")

    flat_records = [flatten_study(study) for study in studies]
    df = pd.DataFrame(flat_records)
    df.to_csv(OUT_PATH, index=False)
    print(f"Transformed data saved to {OUT_PATH}")
