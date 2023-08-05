import pandas as pd
import numpy as np
from src.geeda.column.is_categorical import is_categorical


def is_pseudo_categorical(
    column: pd.Series, bins: int = None, max_threshold: float = 0.3, dropna: bool = True
):
    """
    Identify if the given column is of a pseudo-categorical data type.
    Pseudo-categorical is defined as numeric values that appear categorical after binning is applied.


    Args:
        column (pd.Series): _description_
        max_threshold (float, optional): _description_. Defaults to 0.3.
        dropna (bool, optional): _description_. Defaults to True.
    """
    if bins is None:
        bins = column.size

    # Replace inf values with nan
    # Drop inf values and not nan? Right now they're dropped by is_categorical if dropna is true
    column.replace([np.inf, -np.inf], np.nan, inplace=True)

    binned_column = pd.cut(column, bins)

    return is_categorical(binned_column, max_threshold, dropna)
