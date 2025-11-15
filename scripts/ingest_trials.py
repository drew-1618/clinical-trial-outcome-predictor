"""
Entrypoint to ingest clinical trial data from ClinicalTrials.gov.
"""

from src.pipelines.ingest_trials import run_ingestion_pipeline

SEARCH_CONDITION = "cancer"
PAGE_SIZE = 100
MAX_PAGES = 5

if __name__ == "__main__":
    run_ingestion_pipeline(
        condition=SEARCH_CONDITION,
        page_size=PAGE_SIZE,
        max_pages=MAX_PAGES
    )
