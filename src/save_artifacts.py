import os
import joblib
import pandas as pd


def save_artifacts(models, df_final):
    """
    Save trained model files into root /models folder
    """

    # -------------------------------
    # 1. ROOT PATH DETECTION
    # -------------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR = os.path.join(BASE_DIR, "models")

    os.makedirs(MODEL_DIR, exist_ok=True)

    # -------------------------------
    # 2. BEST MODEL
    # -------------------------------
    best_model = models['XGBoost']

    # -------------------------------
    # 3. SAVE FILES
    # -------------------------------
    joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))

    feature_columns = df_final.drop('price', axis=1).columns.tolist()
    joblib.dump(feature_columns, os.path.join(MODEL_DIR, "feature_columns.pkl"))

    sample_input = df_final.drop('price', axis=1).head(1)
    joblib.dump(sample_input, os.path.join(MODEL_DIR, "sample_input.pkl"))

    print("✅ All deployment artifacts saved inside root /models folder")