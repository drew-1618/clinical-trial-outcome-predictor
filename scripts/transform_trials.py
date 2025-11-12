"""

scripts/transform_trials.py
--------------------------
Script to transform raw clinical trial data
into a structured format for analysis.

"""

import json
import pandas as pd

RAW_PATH = "data/raw/clinical_trials.json"
OUT_PATH = "data/processed/clinical_trials.csv"

def flatten_study(study):
    """Extract a flat dictionary of useful trial info from a nested JSON record"""
    id = study.get("protocolSection", {}).get("identificationModule", {}).get("nctId")
    phase = study.get("protocolSection", {}).get("designModule", {}).get("phases", [])
    status = study.get("protocolSection", {}).get("statusModule", {}).get("overallStatus")
    enrollment = study.get("protocolSection", {}).get("designModule", {}).get("enrollmentInfo", {}).get("count")
    condition = study.get("protocolSection", {}).get("conditionsModule", {}).get("conditions", [])
    sponsor = study.get("protocolSection", {}).get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name")

    return {
        "nct_id": id,
        "phase": ", ".join(phase) if isinstance(phase, list) else phase,
        "status": status,
        "enrollment": enrollment,
        "conditions": ", ".join(condition) if isinstance(condition, list) else condition,
        "sponsor": sponsor,
    }

def main():
    with open(RAW_PATH, "r") as f:
        data = json.load(f)
    
    # Handle both list and dict formats
    if isinstance(data, list):
        studies = data
    elif isinstance(data, dict) and "studies" in data:
        studies = data["studies"]
    else:
        raise ValueError("Unexpected JSON format — could not find studies list")

    flat_records = [flatten_study(study) for study in studies]
    df = pd.DataFrame(flat_records)
    df.to_csv(OUT_PATH, index=False)
    print(f"Transformed data saved to {OUT_PATH}")

if __name__ == "__main__":
    main()
