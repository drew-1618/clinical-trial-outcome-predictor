# scripts/inspections/run_audit_processed.py
"""
Entrypoint to audit cleaned clinical trial data.
"""

import sys
import os

# Add project root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.config_loader import load_config
from src.inspections.audit_processed import audit_processed_data

if __name__ == "__main__":
    config = load_config('paths.yaml')
    processed_path = config['data']['processed']
    audit_processed_data(processed_path)
