# Create virtual environment and install dependencies
setup:
	python -m venv .venv
	. .venv/bin/activate; pip install --upgrade pip
	. .venv/bin/activate; pip install -r requirements.txt

# Run data ingestion
ingest:
	. .venv/bin/activate; python scripts/ingest_trials.py

# Inspect ingested data
inspect_ingested:
	. .venv/bin/activate; python scripts/inspections/inspect_ingested_data.py

# Run data transformation
transform:
	. .venv/bin/activate; python scripts/transform_trials.py

inspect_transformed:
	. .venv/bin/activate; python scripts/inspections/inspect_transformed_data.py

# Run preprocessing pipeline
preprocess:
	. .venv/bin/activate; python src/pipelines/data_preprocessing.py

# Run model training
train:
	. .venv/bin/activate; python src/pipelines/train_model.py

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
