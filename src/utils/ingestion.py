# src/utils/ingestion.py
"""
Ingestion utilities for pulling clinical trial metadata from ClinicalTrials.gov.
"""

import os
import json
import requests

def fetch_trials(api_url, condition, page_size, max_pages):
    """Fetch paginated clinical trial data."""
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
        try:
            response = requests.get(api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break

        studies = data.get("studies", [])
        print(f"   -> Retrieved {len(studies)} studies.")
        all_trials.extend(studies)

        page_token = data.get("nextPageToken")
        if not page_token:
            print("No more pages to fetch.")
            break

    print(f"Total studies fetched: {len(all_trials)}")
    return all_trials


def save_trials(trials, output_path):
    """Save fetched trials to a JSON file."""
    if not trials:
        print("No trials to save.")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(trials, f, indent=2)

    print(f"Saved {len(trials)} studies to {output_path}")
