"""Data loader module for fraud detection.

Provides functions to load raw datasets (CSV and Parquet) and to perform
stratified or chronological train/test splits.
"""

from pathlib import Path
from typing import Optional, Tuple, Union

import pandas as pd
from sklearn.model_selection import train_test_split


def load_raw_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """Load raw dataset from CSV or Parquet format.

    Args:
        file_path: Path to the dataset file.

    Returns:
        pd.DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is not supported.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path.resolve()}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    elif suffix == ".parquet":
        return pd.read_parquet(path)
    else:
        raise ValueError(
            f"Unsupported file format '{suffix}'. Supported formats: .csv, .parquet"
        )


def split_data(
    df: pd.DataFrame,
    target_col: str,
    test_size: float = 0.2,
    time_col: Optional[str] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into train and test sets.

    If `time_col` is None:
        Performs a stratified random split based on the target column.
    If `time_col` is provided:
        Performs a chronological split by sorting chronologically and placing
        the earliest observations into train and latest into test without shuffling.

    Args:
        df: Input DataFrame.
        target_col: Name of the target column.
        test_size: Proportion of the dataset to include in the test split.
        time_col: Optional column name representing transaction timestamp/time.

    Returns:
        Tuple of (X_train, X_test, y_train, y_test).
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in DataFrame.")

    if time_col is not None:
        if time_col not in df.columns:
            raise ValueError(f"Time column '{time_col}' not found in DataFrame.")
        # Chronological split: sort by time_col without shuffling
        df_sorted = df.sort_values(by=time_col).reset_index(drop=True)
        split_idx = int(len(df_sorted) * (1.0 - test_size))

        train_df = df_sorted.iloc[:split_idx]
        test_df = df_sorted.iloc[split_idx:]

        X_train = train_df.drop(columns=[target_col])
        X_test = test_df.drop(columns=[target_col])
        y_train = train_df[target_col]
        y_test = test_df[target_col]
        return X_train, X_test, y_train, y_test
    else:
        # Stratified split
        X = df.drop(columns=[target_col])
        y = df[target_col]
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            stratify=y,
            random_state=42,
        )
        return X_train, X_test, y_train, y_test
