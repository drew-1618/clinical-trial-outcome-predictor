# scripts/run_transformation.py
"""
Entry point to transform raw clinical trial data.
"""

import sys
import os

# Add project root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config_loader import load_config
from src.pipelines.data_transformation import run_transformation_pipeline

if __name__ == "__main__":
    config = load_config('paths.yaml')

    input_file = config['data']['raw']
    output_file = config['data']['interim']

    run_transformation_pipeline(input_file, output_file)
