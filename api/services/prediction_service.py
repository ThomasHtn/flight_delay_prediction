import joblib

model_path = "/ml/models_artifact/lightgbm_model.pkl"
preprocessor_path = "/ml/models_artifact/lightgbm_preprocessor.pkl"

model = None
preprocessor = None
model_loaded = False

try:
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    model_loaded = True
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Model loading failed: {e}")
