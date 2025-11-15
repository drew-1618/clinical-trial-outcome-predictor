"""
Entrypoint to audit cleaned clinical trial data.
"""

from pathlib import Path
from src.inspections.audit_dataframe import audit_dataframe

DATA_PATH = Path("data/processed/cleaned_trials.csv")

if __name__ == "__main__":
    audit_dataframe(DATA_PATH)
