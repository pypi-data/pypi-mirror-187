import pandas as pd
from typing import List


def check_duplicates(df: pd.DataFrame, columns: List[str]) -> int:
    """
    Quantify the amount of duplicate rows (for the target columns)
    present in the given DataFrame.

    Args:
        df (pd.DataFrame):
            The DataFrame to analyze
        columns (List[str]):
            The target columns of interest

    Returns:
        int:
            The number of duplicate rows present
    """
    df = df[columns]
    print(df.drop_duplicates(subset=columns))
    return len(df) - len(df.drop_duplicates())
