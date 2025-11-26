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
	. .venv/bin/activate; python -m scripts.run_training

# =============================
# Testing
# =============================

test:
	. .venv/bin/activate; pytest -v

# =============================
# Run Docker and open
# browser to FastAPI app
# =============================
docker-run:
	@echo "🐳 Building and Starting Docker container..."
	docker-compose -f docker/docker-compose.yml up -d --build
	@echo "⏳ Waiting for API to launch..."
	@sleep 5
	@echo "🚀 Opening Browser..."
	cmd.exe /C start http://localhost:8000/docs || echo "⚠️ Could not open browser automatically. Please click: http://localhost:8000/docs"
	@echo "✅ API is running in the background."
	@echo "   - To stop it: make docker-stop"
	@echo "   - To see logs: make docker-logs"

docker-stop:
	@echo "🛑 Stopping Docker container..."
	docker-compose -f docker/docker-compose.yml down
	@echo "✅ Docker container stopped."

docker-logs:
	@echo "📜 Tailing Docker logs..."
	docker-compose -f docker/docker-compose.yml logs -f
