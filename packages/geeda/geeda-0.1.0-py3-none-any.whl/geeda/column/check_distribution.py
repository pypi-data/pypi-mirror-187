import pandas as pd
from scipy import stats
from typing import Tuple


def is_significant(p_value: float, alpha: float = 0.05) -> bool:
    """
    Check if the statistical test result is significant.

    Args:
        p_value (float):
            The p-value of the statistical test
        alpha (float, optional):
            The alpha level to compare the p-value to, defaults to 0.05.

    Returns:
        bool:
            True if the p-value is less than or equal to alpha, False otherwise
    """
    return p_value <= alpha


def check_distribution(column: pd.Series, alpha: float = 0.05) -> str:
    # Use stats.kstest() for uniform, shapiro_wilk for normal
    mean = column.mean()
    std = column.std()
    size = column.size

    # Normality Test
    shapiro_significant = is_significant(stats.shapiro(column).pvalue, alpha)
    normality = "not normal" if shapiro_significant else "normal"

    # Uniformity Test
    uniform = stats.uniform.rvs(loc=mean, scale=std, size=size, random_state=1)
    ks_significant = is_significant(stats.kstest(rvs=column, cdf=uniform).pvalue, alpha)
    uniformity = "not uniform" if ks_significant else "uniform"

    return f"{normality}, {uniformity}"
