# scripts/inspections/run_inspect_raw.py
"""
Entrypoint to inspect raw ingested JSON data.
"""

import sys
import os

# Add project root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.config_loader import load_config
from src.inspections.inspect_raw import inspect_raw_json

if __name__ == "__main__":
    config = load_config('paths.yaml')
    raw_path = config['data']['raw']
    inspect_raw_json(raw_path)
