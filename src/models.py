"""Model definitions for fraud detection baseline and benchmarks.

Provides baseline Logistic Regression, Random Forest, and XGBoost models
configured for imbalanced classification.
"""

from typing import Any, Dict

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


def get_models(scale_pos_weight: float = 1.0) -> Dict[str, Any]:
    """Instantiate and return baseline and tree-based models.

    Args:
        scale_pos_weight: Ratio of negative to positive samples, used by XGBoost
            to balance positive class weights.

    Returns:
        Dictionary mapping model names to un-fitted estimator instances:
        - "logistic_regression": LogisticRegression with class_weight="balanced"
        - "random_forest": RandomForestClassifier with class_weight="balanced"
        - "xgboost": XGBClassifier with scale_pos_weight
    """
    return {
        "logistic_regression": LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=100,
            class_weight="balanced",
            random_state=42,
        ),
        "xgboost": XGBClassifier(
            n_estimators=100,
            scale_pos_weight=scale_pos_weight,
            eval_metric="logloss",
            random_state=42,
        ),
    }
