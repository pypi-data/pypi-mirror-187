from re import I
import pandas as pd

from geeda.dataframe.geeda import Geeda
from geeda.column.is_categorical import is_categorical
from geeda.column.check_inf import check_inf
from geeda.dataframe.check_duplicates import check_duplicates
from geeda.utils import print_df


df = pd.DataFrame(
    {
        "a": range(1, 7),
        "b": range(5, 11),
        "c": [1, 2, 2, 1, 1, 1],
        "d": [1, 2, 3, 1, 4, 1],
    }
)

# Arrange
geeda = Geeda(df)

# Act
col, df = geeda.apply([is_categorical, check_inf, check_duplicates], ["d", "c"])
