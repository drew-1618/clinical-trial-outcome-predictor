# tests/test_features.py

import pandas as pd
import numpy as np
from src.features.build_features import clean_enrollment_column


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
