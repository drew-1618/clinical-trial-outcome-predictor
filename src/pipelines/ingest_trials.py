"""
Pipeline wrapper for fetching and saving raw clinical trial data.
"""

from src.utils.ingestion import fetch_trials, save_trials

def run_ingestion_pipeline(condition="cancer", page_size=100, max_pages=5):
    trials = fetch_trials(condition=condition, page_size=page_size, max_pages=max_pages)
    save_trials(trials)
    print("Ingestion pipeline complete.")
