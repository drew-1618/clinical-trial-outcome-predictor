# src/inspections/inspect_raw.py

import json
import os
import sys

def inspect_raw_json(filename):
    print(f"Inspecting raw data at: {filename}...")

    if not os.path.exists(filename):
        print(f"File not found at {filename}")
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        trials = []
        structure_type = "unknown"

        if isinstance(data, list):
            trials = data
            structure_type = "List of Studies"
        elif isinstance(data, dict) and 'studies' in data:
            trials = data['studies']
            structure_type = "Dict with 'studies' key"
        else:
            print("Warning: JSON structure not recognized (expected list or dict with 'studies').")
            return

        # basic stats
        print(f"\n1. Structure Type: {structure_type}")
        print(f"2. Total Records: {len(trials)}")

        if trials:
            first_record = trials[0]
            print(f"\n 3. Sample Record Keys: {list(first_record.keys())}")
            print(f"\n 4. Sample Content (First 500 chars): {json.dumps(first_record, indent=2)[:500]}\n...[truncated]")
        else:
            print("\n3. Warning: Trials list is empty.")

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. The file might be corrupt or incomplete.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
