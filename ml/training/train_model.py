import os
import sys

import joblib
import mlflow
import mlflow.sklearn
import optuna
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)

# ───────────────────────────────────────────────────────────────
# Setup project path
# ───────────────────────────────────────────────────────────────
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# ───────────────────────────────────────────────────────────────
# Custom Imports
# ───────────────────────────────────────────────────────────────
from database.services.flight_service import load_training_data
from ml.training.models import get_model
from ml.training.preprocessing import preprocessing, split

# ───────────────────────────────────────────────────────────────
# Constants and Configuration
# ───────────────────────────────────────────────────────────────
MODELS_DIR = "ml/models_artifact"
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_TYPES = ["random_forest", "logistic_regression", "lightgbm"]


# ───────────────────────────────────────────────────────────────
# Training Function
# ───────────────────────────────────────────────────────────────
def train_model(params: dict):
    """
    Load data, preprocess it, train a model, compute metrics,
    and save both model and preprocessor to disk.
    """
    df = load_training_data()

    # Define feature types
    numerical_cols = [
        "month",
        "day_of_week",
        "crs_dep_time",
        "crs_arr_time",
        "crs_elapsed_time",
        "distance",
    ]
    categorical_cols = ["unique_carrier", "origin", "dest", "dep_time_blk"]
    target_col = "arr_del15"

    y_raw = df[target_col]

    # Preprocess input data
    X_processed, y, preprocessor = preprocessing(
        df, numerical_cols, categorical_cols, y_raw
    )
    X_train, X_test, y_train, y_test = split(X_processed, y)

    # Train selected model
    model = get_model(params)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
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


# ───────────────────────────────────────────────────────────────
# Optuna Objective Function for LightGBM
# ───────────────────────────────────────────────────────────────
def objective(trial):
    """
    Objective function for Optuna to optimize LightGBM hyperparameters.
    """
    params = {
        "model_type": "lightgbm",
        "lgbm_n_estimators": trial.suggest_int("lgbm_n_estimators", 50, 300),
        "lgbm_max_depth": trial.suggest_int("lgbm_max_depth", 3, 15),
    }

    _, _, metrics, _ = train_model(params)
    return metrics["f1_score"]


# ───────────────────────────────────────────────────────────────
# Main Training Loop
# ───────────────────────────────────────────────────────────────
def main():
    """
    Train and evaluate multiple models.
    Log results and artifacts to MLflow.
    """
    mlflow.set_experiment("flight_delay_models")

    for model_type in MODEL_TYPES:
        print(f"\n🚀 Training model: {model_type}")

        # Default hyperparameters for each model
        if model_type == "random_forest":
            params = {"model_type": model_type, "n_estimators": 100, "max_depth": 10}

        elif model_type == "logistic_regression":
            params = {"model_type": model_type, "logreg_C": 1.0}

        elif model_type == "lightgbm":
            print("🎯 Running Optuna for LightGBM...")
            study = optuna.create_study(direction="maximize")
            study.optimize(objective, n_trials=10)
            print(f"✅ Best trial score: {study.best_trial.value}")
            print(f"✅ Best hyperparameters: {study.best_trial.params}")
            params = {**study.best_trial.params, "model_type": "lightgbm"}

        # Start MLflow tracking
        with mlflow.start_run(run_name=model_type):
            model, preprocessor, metrics, report = train_model(params)

            mlflow.log_params(params)
            for name, value in metrics.items():
                mlflow.log_metric(name, value)

            mlflow.sklearn.log_model(model, artifact_path="model")
            mlflow.sklearn.log_model(preprocessor, artifact_path="preprocessor")

            print(report)
            print("✅ Model and metrics logged to MLflow.")


# ───────────────────────────────────────────────────────────────
# Entry Point
# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
