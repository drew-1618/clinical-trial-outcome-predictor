FROM python:3.12-slim

# set working directory
WORKDIR /app

# copy requirements first
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy rest of application code
COPY src/ src/
COPY config/ config/
COPY scripts/ scripts/

# copy trained models
COPY models/ models/

# create a non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# expose port the app runs
EXPOSE 8000

# define the command to run the app
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
