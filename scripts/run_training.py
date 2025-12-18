# scripts/run_training.py

import sys
import os

# Add project root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.config_loader import load_config  # noqa: E402
from src.pipelines.model_training import run_training_pipeline  # noqa: E402

if __name__ == "__main__":
    paths_config = load_config("paths.yaml")
    params_config = load_config("params.yaml")
    model_type = params_config["model"]["type"]

    if model_type == 'random_forest':
        output_name = "random_forest.pkl"
    else:
        output_name = "logistic_regression.pkl"

    input_file = paths_config["data"]["processed"]
    model_file = os.path.join('models', output_name) # output model path

    run_training_pipeline(input_file, model_file)
