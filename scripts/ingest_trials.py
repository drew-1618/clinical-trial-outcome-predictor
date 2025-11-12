"""

scripts/ingest_trials.py
--------------------------
Script to ingest clinical trial metadata
and save it as a raw JSON file.

"""

import os
import json
import requests
from datetime import datetime

API_URL = "https://clinicaltrials.gov/api/v2/studies"
OUTPUT_PATH = "data/raw/clinical_trials.json"


def fetch_trials(condition="cancer", page_size=100, max_pages=3):
    """Fetch paginated clinical trial data"""
    all_trials = []
    page_token = None

    for page in range(1, max_pages + 1):
        params = {
            "query.cond": condition,
            "format": "json",
            "pageSize": page_size,
            "countTotal": "true" if page == 1 else "false",
        }

        if page_token:
            params["pageToken"] = page_token

        print(f"Fetching page {page} for condition '{condition}'...")

        response = requests.get(API_URL, params=params)
        print("Requesting URL:", response.url)
        response.raise_for_status()
        data = response.json()
        
        studies = data.get("studies", [])
        print(f" → Retrieved {len(studies)} studies.")
        all_trials.extend(studies)

        page_token = data.get("nextPageToken")
        if not page_token:
            print("No more pages to fetch.")
            break

    print(f"Total studies fetched: {len(all_trials)}")
    return all_trials


def save_trials(trials, output_path=OUTPUT_PATH):
    """Save the fetched data to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(trials, f, indent=2)
    print(f"Saved {len(trials)} studies to {output_path}")


def main():
    trials = fetch_trials(condition="cancer", page_size=100, max_pages=5)
    save_trials(trials)
    print("Ingestion complete.")

if __name__ == "__main__":
    main()