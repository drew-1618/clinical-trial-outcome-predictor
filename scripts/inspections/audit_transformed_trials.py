"""
Entrypoint to audit transformed clinical trial data.
"""

from pathlib import Path
from src.inspections.audit_dataframe import audit_dataframe

DATA_PATH = Path("data/processed/clinical_trials.csv")

if __name__ == "__main__":
    audit_dataframe(DATA_PATH)
