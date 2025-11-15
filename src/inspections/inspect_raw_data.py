# src/inspections/inspect_raw_data.py

import json

def inspect_raw_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        trials = data["studies"]
    except Exception:
        if isinstance(data, list):
            trials = data
        else:
            trials = []

    print(f"Loaded {len(trials)} trials.")

    # Peek at one entry
    if trials:
        first = trials[0]
        print(json.dumps(first, indent=2)[:1000])  # show a trimmed sample
