"""Evaluation metrics and visualization for fraud detection.

Implements precision, recall, F1, ROC-AUC, PR-AUC, confusion matrix,
and Precision-Recall curve plotting.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    PrecisionRecallDisplay,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_predictions(
    y_true: Union[np.ndarray, list],
    y_pred: Union[np.ndarray, list],
    y_prob: Union[np.ndarray, list],
) -> Dict[str, Any]:
    """Calculate key classification evaluation metrics for imbalanced fraud data.

    Args:
        y_true: Ground truth binary labels.
        y_pred: Predicted binary labels (0 or 1).
        y_prob: Predicted probabilities for the positive class (class 1).

    Returns:
        Dictionary containing:
        - precision: float
        - recall: float
        - f1: float
        - roc_auc: float
        - pr_auc: float (Average Precision)
        - confusion_matrix: 2x2 ndarray
    """
    return {
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "pr_auc": float(average_precision_score(y_true, y_prob)),
        "confusion_matrix": confusion_matrix(y_true, y_pred),
    }


def plot_precision_recall_curve(
    y_true: Union[np.ndarray, list],
    y_prob: Union[np.ndarray, list],
    save_path: Optional[Union[str, Path]] = None,
) -> PrecisionRecallDisplay:
    """Plot and optionally save the Precision-Recall curve.

    Args:
        y_true: Ground truth binary labels.
        y_prob: Predicted probabilities for the positive class.
        save_path: Optional path to save the generated figure.

    Returns:
        PrecisionRecallDisplay instance.
    """
    display = PrecisionRecallDisplay.from_predictions(y_true, y_prob)

    if save_path is not None:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        display.figure_.savefig(path, bbox_inches="tight")
        plt.close(display.figure_)

    return display
