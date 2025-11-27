# src/api/schemas.py

from pydantic import BaseModel, Field, ConfigDict

class TrialPredictionsRequest(BaseModel):
    nct_id: str = Field(..., description="Trial ID")
    phase: str = Field(..., description="Trial Phase (e.g. 'Phase 3')")
    condition: str = Field(..., description="Condition/Disease")
    sponsor: str = Field(..., description="Lead Sponsor Name")
    enrollment: float = Field(..., description="Estimated Enrollment")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nct_id": "NCT12345678",
                "phase": "Phase 3",
                "condition": "Non-small cell lung cancer",
                "sponsor": "Pfizer",
                "enrollment": 500
            }
        }
    )


class TrialPredictionsResponse(BaseModel):
    prediction: str
    probability: float
    model_used: str
