import pandas as pd
import numpy as np


def check_inf(column: pd.Series) -> int:
    """
    Quantify the amount of infinite values present in the given column.

    Args:
        column (pd.Series):
            The column to analyze

    Returns:
        int:
            The number of infinite values present
    """
    # return np.isinf(column).values.ravel().sum()
    return column.isin([np.inf, -np.inf]).values.sum()
