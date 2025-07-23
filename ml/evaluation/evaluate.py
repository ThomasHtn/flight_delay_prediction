import os
import sys

import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

# ───────────────────────────────────────────────────────────────
# Add project root to path
# ───────────────────────────────────────────────────────────────
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# ───────────────────────────────────────────────────────────────
# Custom Imports
# ───────────────────────────────────────────────────────────────
from database.services.flight_service import load_training_data
from ml.training.preprocessing import preprocessing, split

# ───────────────────────────────────────────────────────────────
# Constants
# ───────────────────────────────────────────────────────────────
MODEL_TYPE = "lightgbm"  # Change this as needed
MODELS_DIR = "ml/models_artifact"
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)


# ───────────────────────────────────────────────────────────────
# Evaluation Function
# ───────────────────────────────────────────────────────────────
def evaluate_model():
    """
    Load model and preprocessor, run evaluation on test data,
    print metrics and save confusion matrix plot.
    """
    print("🔍 Loading data...")
    df = load_training_data()

    # Define features and target
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

    # Load preprocessor and model
    print("📦 Loading model and preprocessor...")
    model_path = os.path.join(MODELS_DIR, f"{MODEL_TYPE}_model.pkl")
    preproc_path = os.path.join(MODELS_DIR, f"{MODEL_TYPE}_preprocessor.pkl")

    if not os.path.exists(model_path) or not os.path.exists(preproc_path):
        raise FileNotFoundError("❌ Model or preprocessor file not found.")

    model = joblib.load(model_path)
    preprocessor = joblib.load(preproc_path)

    # Preprocess data
    X_processed, y, _ = preprocessing(df, numerical_cols, categorical_cols, y_raw)
    _, X_test, _, y_test = split(X_processed, y)

    # Predictions
    print("🔎 Predicting...")
    y_pred = model.predict(X_test)

    # Metrics
    print("📊 Evaluating...")
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
    }

    for k, v in metrics.items():
        print(f"{k.capitalize():<10}: {v:.4f}")

    # Classification report
    print("\n📃 Classification report:")
    print(classification_report(y_test, y_pred, digits=3))

    # Plot confusion matrix
    print("📈 Saving confusion matrix plot...")
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"{MODEL_TYPE} - Confusion Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, f"{MODEL_TYPE}_confusion_matrix.png"))
    plt.close()

    print("✅ Evaluation complete and saved in 'assets/'.")


# ───────────────────────────────────────────────────────────────
# Entry Point
# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    evaluate_model()
