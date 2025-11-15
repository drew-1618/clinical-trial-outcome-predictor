"""
Entrypoint to inspect transformed data.
"""

from pathlib import Path
from src.inspections.inspect_transformed_data import inspect_transformed_df

DATA_PATH = Path("data/processed/clinical_trials.csv")

if __name__ == "__main__":
    inspect_transformed_df(DATA_PATH)
