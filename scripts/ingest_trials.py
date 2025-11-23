# scripts/ingest_trials.py
"""
Entrypoint to ingest clinical trial data from ClinicalTrials.gov.
"""

import sys
import os
import yaml

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config_loader import load_config
from src.pipelines.data_ingestion import run_ingestion_pipeline

if __name__ == "__main__":
    paths_cfg = load_config('paths.yaml')
    params_cfg = load_config('params.yaml')

    run_ingestion_pipeline(
        api_url=params_cfg['ingestion']['api_url'],
        output_path=paths_cfg['data']['raw'],
        condition=params_cfg['ingestion']['condition'],
        page_size=params_cfg['ingestion']['page_size'],
        max_pages=params_cfg['ingestion']['max_pages']
    )
