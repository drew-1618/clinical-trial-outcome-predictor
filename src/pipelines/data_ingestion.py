# src/pipelines/data_ingestion.py

from src.utils.ingestion import fetch_trials, save_trials

def run_ingestion_pipeline(api_url, output_path, condition, page_size, max_pages):
    print("Starting ingestion pipeline...")
    print(f"Target condition: {condition}")

    trials = fetch_trials(
        api_url=api_url,
        condition=condition,
        page_size=page_size, 
        max_pages=max_pages)
    if trials:
        save_trials(trials, output_path)
        print("Ingestion pipeline finished successfully.")
    else:
        print("Warning: No trials were fetched. Nothing was saved.")
