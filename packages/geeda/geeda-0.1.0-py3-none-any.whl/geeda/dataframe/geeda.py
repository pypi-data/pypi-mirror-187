import pandas as pd
from typing import List, Union, Callable, Optional, Tuple
import inspect

from geeda.utils import make_list, validate_columns, print_df


class Geeda:
    """
    Wrapper class for pd.DataFrame to enable efficient EDA.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def apply(
        self,
        eda_functions: Union[Callable, List[Callable]],
        columns: Optional[Union[str, List[str]]] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Apply the given EDA functions on the given columns of the dataframe.

        Args:
            eda_functions (Union[Callable, List[Callable]]):
                The EDA function(s) to apply on the columns
            columns (Optional[Union[str, List[str]]], optional):
                The column(s) to apply the EDA functions on, defaults to all columns in the dataframe

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]:
                A tuple with the first element being the `column_printout` DataFrame and the second element
                being the `df_printout` DataFrame
        """
        columns = (
            self.df.columns
            if columns is None
            else validate_columns(df=self.df, columns=columns)
        )
        eda_funcs: List[Callable] = make_list(eda_functions)

        # Separate column and dataframe functions
        column_functions = []
        df_functions = []
        for function in eda_funcs:
            import_path: str = inspect.getmodule(function).__name__
            if "column" in import_path:
                column_functions.append(function)
            else:
                df_functions.append(function)

        column_results = dict()
        column_printout_idx = [function.__name__ for function in column_functions]
        for column in columns:
            single_column_results = []
            for function in column_functions:
                result = function(self.df[column])
                single_column_results.append(result)
            column_results[column] = single_column_results
        column_printout = pd.DataFrame(column_results, index=column_printout_idx)

        df_results = []
        df_printout_idx = [function.__name__ for function in df_functions]
        for function in df_functions:
            result = function(self.df, columns)
            df_results.append(result)
        df_printout = pd.DataFrame({"results": df_results}, index=df_printout_idx)

        # Print results
        print("\nColumn-wise EDA Results")
        print_df(column_printout)
        print("\nDF-wise EDA Results")
        print_df(df_printout)

        return column_printout, df_printout
