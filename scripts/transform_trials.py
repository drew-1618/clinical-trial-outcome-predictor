# scripts/transform_trials.py
"""
Entry point to transform raw clinical trial data.
"""

from src.pipelines.transform import transform_trials

if __name__ == "__main__":
    transform_trials()
