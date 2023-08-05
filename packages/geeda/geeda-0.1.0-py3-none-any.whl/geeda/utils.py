import pandas as pd
from typing import List, Union, Any
from tabulate import tabulate


def make_list(input: Union[List[Any], Any]) -> List[Any]:
    """
    Returns the input wrapped in a list if it isn't already a list.

    Args:
        input (Any):
            Any object

    Returns:
        List[Any]:
            The input object wrapped in a list if it isn't already a list
    """
    if not isinstance(input, list):
        input = [input]
    return input


def validate_columns(df: pd.DataFrame, columns: Union[str, List[str]]) -> List[str]:
    """
    Validate that the given column(s) is/are in the given dataframe.

    Args:
        df (pd.DataFrame):
            The dataframe to check columns in
        columns (Union[str, List[str]]):
            The column(s) to check for in the dataframe

    Raises:
        KeyError:
            If one or more columns are not present in the dataframe

    Returns:
        List[str]:
            The column(s) if all were validated successfully
    """
    columns = make_list(columns)
    df_columns = df.columns

    missing_columns = []
    for column in columns:
        if column not in df_columns:
            missing_columns.append(column)
    if len(missing_columns) > 0:
        raise KeyError(f"Column(s) {missing_columns} is/are not in the DataFrame")
    return columns


def print_df(df: pd.DataFrame) -> None:
    """
    Print a DataFrame in a structured format.

    Args:
        df (pd.DataFrame):
            DataFrame to print
    """
    print(tabulate(df, headers="keys", tablefmt="pretty"))
