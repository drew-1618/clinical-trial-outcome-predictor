# src/features/build_features.py

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_phase_column(df):
    """Standardize the 'phase' column to consistent categories."""
    # Fill NaNs with unique category to preserve data
    df['phase'] = df['phase'].fillna('NOT_SPECIFIED')

    # Create binary column for each major phase
    major_phases = ['PHASE1', 'PHASE2', 'PHASE3', 'PHASE4']
    for phase in major_phases:
        df[f'is_{phase.lower()}'] = df['phase'].apply(
            lambda x: 1 if phase in str(x).upper().replace(" ", "") else 0
        )

    df['is_phase_not_specified'] = df['phase'].apply(lambda x: 1 if x == 'NOT_SPECIFIED' else 0)

    # Drop original messy phase column
    df = df.drop(columns=['phase'])
    return df


def clean_enrollment_column(df):
    """
    Imputes missing enrollment values with the median enrollment
    and applies a log transforation to normalize the distribution.
    """
    # Calculate median
    median_val = df['enrollment'].median()
    df['enrollment'] = df['enrollment'].fillna(median_val)

    # Handle zero enrollment since Log(0) is undefined
    df['enrollment_log'] = np.log1p(df['enrollment'])

    # Drop original enrollment column
    df = df.drop(columns=['enrollment'])
    return df


def encode_target_status(df):
    """
    Encode 'status' column into binary target variable.
    0: TERMINATED (Failure)
    1: COMPLETED (Success)
    """
    # Initialize target column with NaNs
    df['target_outcome'] = np.nan

    # Map TERMINATED to 0
    df.loc[df['status'] == 'TERMINATED', 'target_outcome'] = 0
    # Map COMPLETED to 1
    df.loc[df['status'] == 'COMPLETED', 'target_outcome'] = 1
    
    # Drop rows where target is NaN (e.g., 'UNKNOWN', 'RECRUITING', 'WITHDRAWN')
    df = df.dropna(subset=['target_outcome']).copy()
    df['target_outcome'] = df['target_outcome'].astype(int)
    
    df = df.drop(columns=['status'])
    return df


def build_sponsor_features(df, top_n=20, save_path=None):
    """
    One-hot encodes the top N most frequent sponsors and groups the rest.
    If save_path is provided, saves the list of top sponsors for API to use"""

    # Identify top_n sponsors based on counts
    top_sponsors = df['sponsor'].value_counts().head(top_n).index.tolist()

    # save artifact
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(top_sponsors, save_path)
        print(f"   -> Saved top sponsors list to {save_path}")

    # Create new column identifying the top sponsors or other sponsor
    df['sponsor_group'] = df['sponsor'].apply(
        lambda x: x if x in top_sponsors else 'OTHER_SPONSOR'
    )

    # One-hot encode sponsor groups, create column for each group
    df_dummies = pd.get_dummies(df['sponsor_group'], prefix='sponsor', drop_first=False)
    # Merge dummy columns back into main df
    df = pd.concat([df, df_dummies], axis=1)

    # Drop original sponsor columns and temp sponsor_group column
    df = df.drop(columns=['sponsor', 'sponsor_group'])
    return df

def build_conditions_feature(df, max_features=100, save_path=None):
    """
    Applies TF-IDF Vectorization to the conditions column.
    If save_path is provided, saves the fitted Vectorizer for the API to use.
    """
    print(f"   -> Vectorizing 'conditions' using TF-IDF (top {max_features} features)...")

    # Init vectorizer
    tfidf = TfidfVectorizer(
        stop_words='english', lowercase=True, max_features=max_features,
        ngram_range=(1, 2)  # consider 1-word and 2-word phrases
    )

    # Fit and transform the 'conditions' text
    matrix = tfidf.fit_transform(df['conditions'].fillna('')).toarray()

    # save artifact
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(tfidf, save_path)
        print(f"   -> Saved TF-IDF vectorizer to {save_path}")

    feature_names = [f'cond_{name}' for name in tfidf.get_feature_names_out()]

    df_conditions = pd.DataFrame(matrix, columns=feature_names, index=df.index)

    df = pd.concat([df, df_conditions], axis=1)

    # Drop original conditions column
    df = df.drop(columns=['conditions'])
    return df
