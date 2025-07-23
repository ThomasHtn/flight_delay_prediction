import os
import sys

import joblib
import mlflow
import mlflow.sklearn
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from database.services.flight_service import load_training_data
from ml.training.models import get_model
from ml.training.preprocessing import preprocessing, split

# Path to save trained models
MODELS_DIR = "ml/models"
os.makedirs(MODELS_DIR, exist_ok=True)

# List of model types to train
MODEL_TYPES = ["random_forest", "logistic_regression", "svm"]


def train_model(params: dict):
    """
    Train a classification model based on given parameters.
    Saves both the model and its preprocessor to disk.
    """
    df = load_training_data()

    numerical_cols = [
        "month",
        "day_of_week",
        "crs_dep_time",
        "crs_arr_time",
        "crs_elapsed_time",
        "distance",
    ]
    categorical_cols = [
        "unique_carrier",
        "origin",
        "dest",
        "dep_time_blk",
    ]
    target_col = "arr_del15"
    y_raw = df[target_col]

    # Preprocess data
    X_processed, y, preprocessor = preprocessing(
        df, numerical_cols, categorical_cols, y_raw
    )
    X_train, X_test, y_train, y_test = split(X_processed, y)

    # Train model
    model = get_model(params)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Compute metrics
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
    }

    # Save model and preprocessor
    joblib.dump(model, os.path.join(MODELS_DIR, f"{params['model_type']}_model.pkl"))
    joblib.dump(
        preprocessor,
        os.path.join(MODELS_DIR, f"{params['model_type']}_preprocessor.pkl"),
    )

    report = classification_report(y_test, y_pred, digits=3)
    return model, preprocessor, metrics, report


def main():
    """
    Train and evaluate all defined models.
    Log results to MLflow.
    """
    mlflow.set_experiment("flight_delay_models")

    for model_type in MODEL_TYPES:
        print(f"\n🚀 Training model: {model_type}")

        # Define parameters based on model type
        if model_type == "random_forest":
            params = {
                "model_type": model_type,
                "n_estimators": 100,
                "max_depth": 10,
            }
        elif model_type == "logistic_regression":
            params = {"model_type": model_type, "logreg_C": 1.0}
        elif model_type == "svm":
            params = {"model_type": model_type, "svm_C": 1.0, "svm_kernel": "rbf"}

        with mlflow.start_run(run_name=model_type):
            model, preprocessor, metrics, report = train_model(params)

            # Log parameters and metrics
            mlflow.log_params(params)
            for metric_name, value in metrics.items():
                mlflow.log_metric(metric_name, value)

            # Log model and preprocessing pipeline
            mlflow.sklearn.log_model(model, artifact_path="model")
            mlflow.sklearn.log_model(preprocessor, artifact_path="preprocessor")

            print(report)
            print("✅ Model and metrics logged in MLflow.")


if __name__ == "__main__":
    main()
