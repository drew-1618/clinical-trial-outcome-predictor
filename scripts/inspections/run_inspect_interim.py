# scripts/inspections/run_inspect_interim.py
"""
Entrypoint to inspect transformed data.
"""

import sys
import os

# Add project root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.config_loader import load_config  # noqa: E402
from src.inspections.inspect_interim import inspect_interim_df  # noqa: E402

if __name__ == "__main__":
    config = load_config("paths.yaml")
    interim_path = config["data"]["interim"]
    inspect_interim_df(interim_path)
