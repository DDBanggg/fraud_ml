"""Feature preprocessing module for fraud detection.

Builds scikit-learn preprocessing pipelines for numeric and categorical columns.
"""

from typing import List

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, RobustScaler


def build_preprocessor(
    numeric_cols: List[str],
    categorical_cols: List[str],
) -> ColumnTransformer:
    """Build a ColumnTransformer for tabular preprocessing.

    Uses RobustScaler for numerical features to handle outliers common in
    transaction amounts, and OneHotEncoder with handle_unknown='ignore' for
    categorical features.

    Args:
        numeric_cols: List of numerical column names.
        categorical_cols: List of categorical column names.

    Returns:
        Unfitted ColumnTransformer instance.
    """
    transformers = [
        ("num", RobustScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ]
    return ColumnTransformer(transformers=transformers)
