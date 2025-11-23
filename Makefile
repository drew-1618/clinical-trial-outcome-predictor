# =============================
# Set up & Environment
# =============================
.PHONY: setup clean lint format

setup:
	python -m venv .venv
	. .venv/bin/activate; pip install --upgrade pip
	. .venv/bin/activate; pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf mlflow/

lint:
	. .venv/bin/activate; flake8 src scripts

format:
	. .venv/bin/activate; black src scripts

# =============================
# Data Pipeline
# =============================
.PHONY: ingest inspect_raw transform prepare

# Ingest: JSON -> raw CSV
ingest:
	. .venv/bin/activate; python -m scripts.ingest_trials

inspect_raw:
	. .venv/bin/activate; python -m scripts.inspections.run_inspect_raw

# Transform: Raw -> Interim CSV (Flattening)
transform:
	. .venv/bin/activate; python -m scripts.run_transformation

inspect_interim:
	. .venv/bin/activate; python -m scripts.inspections.run_inspect_interim

# Prepare: Interim -> Processed CSV (Cleaning + Features)
prepare:
	. .venv/bin/activate; python -m scripts.run_preparation

audit_processed:
	. .venv/bin/activate; python -m scripts.inspections.run_audit_processed

# =============================
# Model Pipeline
# =============================
.PHONY: train

train:
	. .venv/bin/activate; python -m src.pipelines.train_model

# =============================
# Testing
# =============================

test:
	. .venv/bin/activate; pytest -v
