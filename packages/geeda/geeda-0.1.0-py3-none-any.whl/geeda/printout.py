from typing import List, Dict, Any
from src.geeda.utils import print_df


class Printout:
    """
    Wrapper for dict of check/metric mapped to results?
    """

    def __init__(
        self,
        columns: List[str],
        column_results: Dict[str, List[Any]],
        df_results: Dict[str, Any],
    ) -> None:
        self.columns = columns
        self.column_results = column_results
        self.df_results = df_results

    def printout(self):
        print("Column-wise EDA Results")
        print_df(self.column_printout)
        print("DF-wise EDA Results")
        print_df(self.df_printout)
