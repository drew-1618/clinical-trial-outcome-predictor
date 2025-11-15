# src/utils/flattening.py

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
