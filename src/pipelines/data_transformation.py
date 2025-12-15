# src/pipelines/data_transformation.py

import json
import os
import pandas as pd

from src.utils.flattening import flatten_study


def run_transformation_pipeline(input_path, output_path):
    print(f"Loading raw data from {input_path}...")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Raw data file not found: {input_path}")

    with open(input_path, "r") as f:
        data = json.load(f)

    # Handle both list and dict formats
    if isinstance(data, list):
        studies = data
    elif isinstance(data, dict) and "studies" in data:
        studies = data["studies"]
    else:
        raise ValueError("Unexpected JSON format — " "could not find studies list")

    print(f"Flattening {len(studies)} studies...")
    flat_records = [flatten_study(study) for study in studies]
    df = pd.DataFrame(flat_records)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Transformed data saved to {output_path}")
