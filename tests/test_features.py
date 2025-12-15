# tests/test_features.py

import pandas as pd
import numpy as np
from src.features.build_features import (
    clean_phase_column,
    clean_enrollment_column,
    encode_target_status,
    build_sponsor_features
)

def test_enrollment_log_trasform():
    """Check that enrollment is correctly log-transformed and handles NaNs"""
    # create sample data
    df = pd.DataFrame({
        'enrollment' : [0, 10, 100, np.nan, 5000]
    })
    # run function
    df_processed = clean_enrollment_column(df)

    # column should be renamed
    assert 'enrollment_log' in df_processed.columns
    assert 'enrollment' not in df_processed.columns

    # log(0+1) = 0
    assert df_processed.iloc[0]['enrollment_log'] == 0.0
    # log(10+1) = ~2.39
    assert np.isclose(df_processed.iloc[1]['enrollment_log'], np.log1p(10))
    # log(100+1) = ~4.62
    assert np.isclose(df_processed.iloc[2]['enrollment_log'], np.log1p(100))

    # NaN should be filled with median (which is 55 here)
    # [0, 10, 100, 5000] 
    assert np.isclose(df_processed.iloc[3]['enrollment_log'], np.log1p(55))


def test_clean_phase_columns():
    """Check that phases are correctly mapped to binary columns"""
    df = pd.DataFrame({
        'phase': ['Phase 3', 'Phase 1/Phase 2', 'Not Applicable', None]
    })
    df_processed = clean_phase_column(df)

    # check phase 3 row
    assert df_processed.iloc[0]['is_phase3'] == 1
    assert df_processed.iloc[0]['is_phase1'] == 0

    # check mixed phase row
    assert df_processed.iloc[1]['is_phase1'] == 1
    assert df_processed.iloc[1]['is_phase2'] == 1

    # check null handling
    assert df_processed.iloc[3]['is_phase_not_specified'] == 1


def test_encode_target_status():
    """Check that target status is COMPLETED=1, TERMINATED=0, and others are dropped"""
    df = pd.DataFrame({
        'status': ['COMPLETED', 'TERMINATED', 'WITHDRAWN', 'RECRUITING']
    })
    df_processed = encode_target_status(df)

    # should only have two rows left
    assert df_processed.shape[0] == 2

    # verify values
    # can't use iloc since rows may be reordered after dropna
    assert 1 in df_processed['target_outcome'].values  # COMPLETED
    assert 0 in df_processed['target_outcome'].values  # TERMINATED

    # verify original column is gone
    assert 'status' not in df_processed.columns


def test_build_sponsor_features():
    """Check that top sponsors get their own column and small ones are grouped"""
    df = pd.DataFrame({
        'sponsor': ['Pfizer'] * 5 + ['TinyBio']
    })
    # run with top_n=1 to isolate
    df_processed = build_sponsor_features(df, top_n=1)

    # should have 'sponsor_Pfizer' and 'sponsor_OTHER_SPONSOR'
    assert 'sponsor_Pfizer' in df_processed.columns
    assert 'sponsor_OTHER_SPONSOR' in df_processed.columns

    # last row (TinyBio) should be 1 in OTHER_SPONSOR
    assert df_processed.iloc[5]['sponsor_OTHER_SPONSOR'] == 1
    assert df_processed.iloc[5]['sponsor_Pfizer'] == 0
