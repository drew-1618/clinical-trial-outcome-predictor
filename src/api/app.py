# src/api/app.py

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
import numpy as np
import joblib
import pandas as pd
import os
import sys

# Add project root to python path so we can import src.utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.config_loader import load_config
from src.api.schemas import *

# keep model in global scope for it to stay in memory
models = {}
artifacts = {}
config = load_config('paths.yaml')

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Dynamic Life-cycle logic:
        Loads ALL models defined in config['models'] automatically.
    """
    print("--- API STARTUP ---")
    # iterate over all model paths in cofig
    for model_name, model_path in config['models'].items():
        if not os.path.exists(model_path):
            print(f"Warning: Model path '{model_path}' does not exist. Skipping...")
            continue

        # load models
        print(f"Loading model '{model_name}' from '{model_path}'...")
        try:
            models[model_name] = joblib.load(model_path)
            print(f"Model '{model_name}' loaded successfully.")
        except Exception as e:
            print(f"Error loading model '{model_name}': {e}")

        # load artifacts (vectorizer & sponsor list)
        for artifact_name, artifact_path in config['artifacts'].items():
            if not os.path.exists(artifact_path):
                print(f"Warning: Artifact path '{artifact_path}' does not exist. Skipping...")
                continue
            print(f"Loading artifact '{artifact_name}' from '{artifact_path}'...")
            try:
                artifacts[artifact_name] = joblib.load(artifact_path)
                print(f"Artifact '{artifact_name}' loaded successfully.")
            except Exception as e:
                print(f"Error loading artifact '{artifact_name}': {e}")


    if not models:
        print("CRITICAL: No models loaded. API will not function correctly.")
    yield

    models.clear()
    artifacts.clear()
    print("--- API SHUTDOWN ---")


# init the app
app = FastAPI(title='Clinical Trial Outcome Predictor', version='1.0', lifespan=lifespan)


# Helper: Transition Layer
def transform_input(request: TrialPredictionsRequest) -> pd.DataFrame:
    """Converts a single API request into the dataframe format expected by the model."""
    data = {}

    # enrollment (log transform)
    val = request.enrollment if request.enrollment > 0 else 0
    data['enrollment_log'] = np.log1p(val)

    # phase (one-hot)
    phases = ['phase1', 'phase2', 'phase3', 'phase4']
    req_phase = request.phase.lower()

    for p in phases:
        data[f'is_{p}'] = 1 if p in req_phase else 0
    
    # check for not specified
    data['is_phase_not_specified'] = 1 if "not specified" in req_phase else 0

    # sponsor (one-hot)
    top_sponsors = artifacts.get('top_sponsors', [])
    sponsor_group = request.sponsor if request.sponsor in top_sponsors else 'OTHER_SPONSOR'

    # init all sponsor cols to 0
    data['sponsor_OTHER_SPONSOR'] = 0
    for s in top_sponsors:
        data[f'sponsor_{s}'] = 0

    # set matching one to 1
    if f'sponsor_{sponsor_group}' in data:
        data[f'sponsor_{sponsor_group}'] = 1

    # conditions (tf-idf using saved vectorizer)
    tfidf = artifacts.get('tfidf_vectorizer')
    if tfidf:
        #  transform returns matrix, convert to array
        vectors = tfidf.transform([request.condition if request.condition else '']).toarray()[0]
        feature_names = tfidf.get_feature_names_out()

        # map to cond_word columns
        for i, name in enumerate(feature_names):
            data[f'cond_{name}'] = vectors[i]

    # convert dict to single-row dataframe
    return pd.DataFrame([data])


@app.get("/health")
def check_health():
    """ Basic health check to verify API is running."""
    return {
        "status" : "healthy" if models else "degraded",
        "models" : list(models.keys()),
        "artifacts" : list(artifacts.keys())
    }


@app.post("/predict", response_model=TrialPredictionsResponse)
def predict(request: TrialPredictionsRequest):
    if "logistic_baseline" not in models:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # transform user input -> model features
    try:
        input_df = transform_input(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Transformation Error: {str(e)}")

    # predict
    model = models['logistic_baseline']

    # get prob of class 1 (success)
    prob = model.predict_proba(input_df)[0][1]
    pred_class = "Success" if prob > 0.5 else "Failure"

    return {
        "prediction": pred_class,
        "probability": round(prob, 4),
        "model_used": "logistic_baseline"
    }
    

@app.get("/", include_in_schema=False)
def root():
    """
    Redirects the root URL to the /docs Swagger UI.
    """
    return RedirectResponse(url="/docs")
