
import pandas as pd
import numpy as np
from scipy import stats


def remove_outliers(df, target_cols, std_dev=2):
    try:
        return df[(np.abs(stats.zscore(df[target_cols])) < std_dev).all(axis=1)]
    except Exception:
        try:
            return df[np.abs(stats.zscore(df[target_cols])) < std_dev]
        except Exception:
            return df[np.abs(stats.zscore(df.values)) < std_dev]

