# 🏥 Clinical Trial Outcome Predictor

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2?logo=mlflow&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Logistic%20Regression-F7931E?logo=scikit-learn&logoColor=white)

## 🎯 Goal
Predict the likelihood that a clinical trial will reach **Completion** versus being **Terminated**, using metadata fetched from the ClinicalTrials.gov API. This project serves as a comprehensive **End-to-End MLOps Template**, demonstrating data engineering, model training, artifact management, and API deployment.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    %% --- Styles ---
    %% High Contrast Mode (Black Text)
    classDef storage fill:#bbdefb,stroke:#0d47a1,stroke-width:2px,color:#000;
    classDef process fill:#e1bee7,stroke:#4a148c,stroke-width:2px,rx:5,ry:5,color:#000;
    classDef artifact fill:#ffecb3,stroke:#ff6f00,stroke-width:2px,rx:5,ry:5,color:#000;
    classDef app fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000;
    classDef source fill:#e0e0e0,stroke:#616161,stroke-width:2px,color:#000;

    %% --- Nodes ---
    
    %% External Source
    Internet([ClinicalTrials.gov]):::source

    %% Data Stores (Blue)
    Raw[(Raw JSON)]:::storage
    Interim[(Interim CSV)]:::storage
    Processed[(Processed CSV)]:::storage
    
    %% Scripts/Processes (Purple)
    Ingest[scripts/ingest_trials]:::process
    Transform[scripts/run_transformation]:::process
    Prepare[scripts/run_preparation]:::process
    Train[scripts/run_training]:::process
    
    %% Artifacts (Orange/Gold)
    Vector([TF-IDF Vectorizer]):::artifact
    Sponsors([Sponsor List]):::artifact
    Model{{Logistic Regression}}:::artifact
    
    %% App (Green)
    API[FastAPI App]:::app
    
    %% --- Flow ---
    
    %% Phase 1: Ingestion & Transformation
    Internet --> Ingest
    Ingest --> Raw
    Raw --> Transform
    Transform --> Interim
    
    %% Phase 2: Preparation & Feature Engineering
    Interim --> Prepare
    Prepare --> Processed
    
    %% Artifact Generation (Side Effects)
    Prepare -.->|<strong style='color:#d50000;padding:10px;font-size:14px;'>Generates</strong>| Vector
    Prepare -.->|<strong style='color:#d50000;padding:10px;font-size:14px;'>Generates</strong>| Sponsors
    
    %% Phase 3: Training
    Processed --> Train
    Train --> Model
    
    %% Phase 4: Serving
    Vector -->|<strong style='color:#d50000;padding:10px;font-size:14px;'>Load</strong>| API
    Sponsors -->|<strong style='color:#d50000;padding:10px;font-size:14px;'>Load</strong>| API
    Model -->|<strong style='color:#d50000;padding:10px;font-size:14px;'>Load</strong>| API
```

---

## ⚡ Key Features

* **Modular Pipeline:** Separation of concerns between Ingestion, Transformation, and Training.
* **Robust Preprocessing:** Handles missing values, log-transforms continuous data, and performs One-Hot Encoding/TF-IDF on categorical text.
* **Experiment Tracking:** Uses **MLflow** to log metrics (ROC-AUC, Precision, Recall) and model parameters.
* **API Serving:** Exposes the model via **FastAPI** with Pydantic validation and automatic Swagger UI documentation.
* **Containerization:** Fully Dockerized for reproducible deployment anywhere.
* **Quality Gates:** Automated data auditing and unit testing via **pytest**.

---

## 📂 Project Structure

```text
├── config/                 # YAML configuration files (paths, params)
├── data/                   # Data storage (gitignored)
│   ├── raw/                # Original JSON from API
│   ├── interim/            # Flattened CSV
│   └── processed/          # Feature-engineered CSV
├── docker/                 # Dockerfile and docker-compose.yml
├── models/                 # Saved artifacts (.pkl, .joblib)
├── scripts/                # Entry points for the pipeline (e.g., run_train.py)
├── src/                    # Source code modules
│   ├── api/                # FastAPI application & schemas
│   ├── features/           # Feature engineering logic
│   ├── inspections/        # Data quality checks & exploratory inspection logic
│   ├── pipelines/          # Core pipeline orchestration
│   └── utils/              # Helper functions (config loading, etc.)
├── tests/                  # Unit tests
├── Makefile                # Command shortcuts
└── requirements.txt        # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.12+
* Docker & Docker Compose (optional, for containerization)

### Local Installation
```bash
# 1. Clone the repository
git clone [https://github.com/drew-1618/clinical-trial-outcome-predictor.git](https://github.com/drew-1618/clinical-trial-outcome-predictor.git)
cd clinical-trial-outcome-predictor

# 2. Setup Virtual Environment & Install Dependencies
make setup
```

---

## 🛠️ Usage

### 🚀 Master Commands (The "Easy Button")
Use these commands to manage the entire lifecycle in one step.

| Command | Description |
| :--- | :--- |
| **`make all`** | **Build Everything:** Runs ingestion, transformation, preparation, auditing, training, and testing in the correct order. |
| **`make clean`** | **Soft Reset Project:** Finds and deletes Python cache files, pytest cache files, and MLFlow logs. |
| **`make nuke`** | **Hard Reset Project:** Deletes all generated data (`data/raw`, `processed`, etc.) and models. Use with caution! |

---

### 1. Run the Data Pipeline
If you need to run specific stages manually:
```bash
make ingest       # Fetch Raw JSON
make transform    # Convert to CSV
make prepare      # Clean & Feature Engineer (Creates artifacts)
```

### 2. Train the Model
Trains a Logistic Regression model and logs results to MLflow.
```bash
make train
```

### 3. Docker Management (Serving)
Commands to manage the containerization API.
| Command | Description |
| :--- | :--- |
| **`make docker-run`** | Builds the image, starts the container, and opens the Swagger UI in your browser automatically. |
| **`make docker-stop`** | Stops and removes the running container (frees up port 8000). |
| **`make docker-logs`** | Tails the server logs (Press `Ctrl+C` to exit). |

### 4. Local Development (No Docker)
Starts the FastAPI server locally.
```bash
uvicorn src.api.app:app --reload
```
* **API URL:** `http://localhost:8000`
* **Documentation:** `http://localhost:8000/docs`

---

## 📡 API Reference

**Endpoint:** `POST /predict`

**Request Body:**
```json
{
  "nct_id": "NCT12345678",
  "phase": "Phase 3",
  "condition": "Non-small cell lung cancer",
  "sponsor": "Pfizer",
  "enrollment": 500
}
```

**Response:**
```json
{
  "prediction": "Success",
  "probability": 0.9372,
  "model_used": "logistic_baseline"
}
```

---

## 🧪 Testing

Run the test suite to verify API endpoints and feature engineering logic.
```bash
pytest
```
