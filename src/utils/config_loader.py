# src/utils/config_loader.py

import os
import yaml
from pathlib import Path

# src/utils/ -> src/ -> PROJECT_ROOT (2 levels up)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"

def load_config(filename):
    file_path = CONFIG_DIR / filename
        
    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found at: {file_path}")
        
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
