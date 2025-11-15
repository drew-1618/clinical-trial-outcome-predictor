# Create virtual environment and install dependencies
setup:
	python -m venv .venv
	. .venv/bin/activate; pip install --upgrade pip
	. .venv/bin/activate; pip install -r requirements.txt

# Run data ingestion
ingest:
	. .venv/bin/activate; python -m scripts.ingest_trials

# Inspect ingested raw data
inspect_ingested:
	. .venv/bin/activate; python -m scripts.inspections.inspect_raw_data

# Run data transformation
transform:
	. .venv/bin/activate; python -m scripts.transform_trials

# Inspect transformed data
inspect_transformed:
	. .venv/bin/activate; python -m scripts.inspections.inspect_transformed_data

# Audit data quality
audit_transformed:
	. .venv/bin/activate; python -m scripts.inspections.audit_transformed_trials
audit_cleaned:
	. .venv/bin/activate; python -m scripts.inspections.audit_cleaned_trials

# Clean/preprocess data
.PHONY: clean_data preprocess
clean_data:
	. .venv/bin/activate; python -m scripts.clean_data
preprocess:
	. .venv/bin/activate; python -m scripts.clean_data

# Run model training
train:
	. .venv/bin/activate; python -m src.pipelines.train_model

# Run tests
test:
	. .venv/bin/activate; pytest -v

# Format code
format:
	. .venv/bin/activate; black .

# Lint
lint:
	. .venv/bin/activate; flake8 .

# Clean caches and temp data
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
