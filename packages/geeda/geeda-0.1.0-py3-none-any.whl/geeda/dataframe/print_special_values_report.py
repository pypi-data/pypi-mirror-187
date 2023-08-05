import pandas as pd
from functools import partial
from enum import Enum
from typing import List

from src.geeda.dataframe.check_nan import check_nan
from src.geeda.dataframe.check_inf import check_inf


class SpecialValue(Enum):
    NaN = partial(check_nan)
    Inf = partial(check_inf)


def print_special_values_report(df: pd.DataFrame, columns: List[str]):
    pass
