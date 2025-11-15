"""
Entrypoint to clean and featurize clinical trial data.
"""

from src.pipelines.clean import run_cleaning_pipeline

RAW_PROCESSED_FILE = 'data/processed/clinical_trials.csv'
CLEANED_FILE = 'data/processed/cleaned_trials.csv'

if __name__ == "__main__":
    run_cleaning_pipeline(RAW_PROCESSED_FILE, CLEANED_FILE)
