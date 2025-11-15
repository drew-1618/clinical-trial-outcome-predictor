# src/features/cleaning.py

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_phase_column(df):
    """Standardize the 'phase' column to consistent categories."""
    # Fill NaNs with unique category to preserve data
    df['phase'] = df['phase'].fillna('NOT_SPECIFIED')

    # Create binary column for each major phase
    major_phases = ['PHASE1', 'PHASE2', 'PHASE3', 'PHASE4']
    for phase in major_phases:
        df[f'is_{phase.lower()}'] = df['phase'].apply(lambda x: 1 if phase in x else 0)
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
    median_enrollment = df['enrollment'].median()
    df['enrollment'] = df['enrollment'].fillna(median_enrollment)

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


def clean_sponsor_column(df, top_n=20):
    """One-hot encodes the top N most frequent sponsors and groups the rest."""

    # Identify top_n sponsors based on counts
    top_sponsors = df['sponsor'].value_counts().head(top_n).index.tolist()

    # Create new column identifying the top sponsors or other sponsor
    def get_sponsor_group(sponsor):
        return sponsor if sponsor in top_sponsors else 'OTHER_SPONSOR'

    df['sponsor_group'] = df['sponsor'].apply(get_sponsor_group)

    # One-hot encode sponsor groups, create column for each group
    df_dummies = pd.get_dummies(df['sponsor_group'], prefix='sponsor', drop_first=False)

    # Merge dummy columns back into main df
    df = pd.concat([df, df_dummies], axis=1)

    # Drop original sponsor columns and temp sponsor_group column
    df = df.drop(columns=['sponsor', 'sponsor_group'])

    return df

def clean_conditions_column(df, max_features=100):
    """Applies TF-IDF Vectorization to the conditions column."""
    print(f"Vectorizing 'conditions' using TF-IDF (top {max_features} features)...")

    # Init vectorizer
    tfidf = TfidfVectorizer(
        stop_words='english',
        lowercase=True,
        max_features=max_features,
        ngram_range=(1, 2)  # consider 1-word and 2-word phrases
    )

    # Fit and transform the 'conditions' text
    conditions_matrix = tfidf.fit_transform(df['conditions']).toarray()

    feature_names = [f'cond_{name}' for name in tfidf.get_feature_names_out()]
    df_conditions = pd.DataFrame(conditions_matrix, columns=feature_names)

    # Reset index of main df
    df = df.reset_index(drop=True)

    df = pd.concat([df, df_conditions], axis=1)

    # Drop original conditions column
    df = df.drop(columns=['conditions'])

    return df
