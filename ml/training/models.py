from typing import Dict

from lightgbm import LGBMClassifier
from sklearn.base import ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# ───────────────────────────────────────────────────────────────
# Model Factory Functions
# ───────────────────────────────────────────────────────────────


def get_random_forest(params: Dict) -> RandomForestClassifier:
    """
    Create a configured RandomForestClassifier instance.
    """
    return RandomForestClassifier(
        n_estimators=params.get("n_estimators", 100),
        max_depth=params.get("max_depth", 10),
        class_weight=params.get("class_weight", None),
        random_state=42,
    )


def get_logistic_regression(params: Dict) -> LogisticRegression:
    """
    Create a configured LogisticRegression instance.
    """
    return LogisticRegression(
        C=params.get("logreg_C", 1.0),
        max_iter=1000,
        class_weight=params.get("class_weight", None),
        solver="liblinear",
    )


def get_lightgbm(params: Dict) -> LGBMClassifier:
    """
    Create a configured LightGBM classifier instance.
    """
    return LGBMClassifier(
        n_estimators=params.get("lgbm_n_estimators", 100),
        max_depth=params.get("lgbm_max_depth", -1),
        class_weight=params.get("class_weight", None),
        random_state=42,
        verbosity=-1,
    )


# ───────────────────────────────────────────────────────────────
# Model Dispatcher
# ───────────────────────────────────────────────────────────────


def get_model(params: Dict) -> ClassifierMixin:
    """
    Return the appropriate classification model instance based on the 'model_type' key in params.
    Supported values: 'random_forest', 'logistic_regression', 'lightgbm'.
    """
    model_type = params.get("model_type", "random_forest")

    if model_type == "random_forest":
        return get_random_forest(params)
    elif model_type == "logistic_regression":
        return get_logistic_regression(params)
    elif model_type == "lightgbm":
        return get_lightgbm(params)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
