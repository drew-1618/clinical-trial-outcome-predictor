# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add project root to python path so we can import from src.api
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.api.app import app

# use fixture with context manager to trigger startup/shutdown events
@pytest.fixture
def client():
    """Create a TestClient instance that triggers the startup/shutdown events"""
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    """Verify the API starts and looks healthy"""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert "logistic_baseline" in json_data["models"]


def test_prediction_success(client):
    """Verify the API can predict 'Success' for a good trial"""
    payload = {
        "nct_id": "NCT12345678",
        "phase": "Phase 3",
        "condition": "Breast Cancer",  # High success rate condition
        "sponsor": "Pfizer",           # Big sponsor
        "enrollment": 1000             # Large trial
    }
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    # check the contract (that the keys exist)
    assert "prediction" in data
    assert "probability" in data
    assert "model_used" in data
    
    # check the schema (data types)
    assert isinstance(data["prediction"], str)
    assert isinstance(data["probability"], float)
    assert isinstance(data["model_used"], str)

    # expect a high chance of success
    assert data["prediction"] == "Success"


def test_prediction_validation_error(client):
    """Verifies the API rejects bad data"""
    bad_payload = {
        "nct_id": "NCT123",
        "phase": "Phase 3",
        "condition": "Flu",
        "sponsor": "Me",
        "enrollment": "Five Hundred" # string instead of float
    }
    
    response = client.post("/predict", json=bad_payload)
    
    assert response.status_code == 422 # validation error
