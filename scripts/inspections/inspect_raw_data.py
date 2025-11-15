"""
Entrypoint to inspect raw ingested JSON data.
"""

from pathlib import Path
from src.inspections.inspect_raw_data import inspect_raw_json

RAW_PATH = Path("data/raw/clinical_trials.json")

if __name__ == "__main__":
    inspect_raw_json(RAW_PATH)
