# scripts/run_preparation.py

"""
Entrypoint to clean and featurize clinical trial data.
"""
import sys
import os

# Add project root to python path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.config_loader import load_config  # noqa: E402
from src.pipelines.data_preparation import run_preparation_pipeline  # noqa: E402

if __name__ == "__main__":
    config = load_config("paths.yaml")

    input_file = config["data"]["interim"]
    output_file = config["data"]["processed"]

    run_preparation_pipeline(input_file, output_file)
