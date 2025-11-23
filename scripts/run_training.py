# scripts/run_training.py

import sys
import os

# Add project root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config_loader import load_config
from src.pipelines.model_training import run_training_pipeline

if __name__ == "__main__":
    config = load_config('paths.yaml')
    input_file = config['data']['processed']
    model_file = config['models']['logistic_baseline']  # output model path

    run_training_pipeline(input_file, model_file)
