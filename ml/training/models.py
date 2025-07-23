from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


def get_model(params: dict):
    """
    Return a classification model instance based on params['model_type'].
    Supported: 'random_forest', 'logistic_regression', 'svm'
    """

    model_type = params.get("model_type", "random_forest")

    if model_type == "random_forest":
        return RandomForestClassifier(
            n_estimators=params.get("n_estimators", 100),
            max_depth=params.get("max_depth", 10),
            class_weight="balanced",
            random_state=42,
        )

    elif model_type == "logistic_regression":
        return LogisticRegression(
            C=params.get("logreg_C", 1.0),
            max_iter=1000,
            class_weight="balanced",
            solver="liblinear",
        )

    elif model_type == "svm":
        return SVC(
            C=params.get("svm_C", 1.0),
            kernel=params.get("svm_kernel", "rbf"),
            class_weight="balanced",
            probability=True,
        )

    else:
        raise ValueError(f"Unsupported model type: {model_type}")
