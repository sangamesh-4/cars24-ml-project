import joblib
import pandas as pd
import os

from src.data_preprocessing import preprocess_data
from src.feature_engineering import feature_engineering


# -------------------------------
# LOAD SAVED MODEL FILES
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODEL_DIR, "best_model.pkl"))
feature_columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.pkl"))


def predict_price(user_input):
    """
    Full end-to-end prediction pipeline
    """

    # -------------------------------
    # 0. AUTO ADD HIDDEN BACKEND VALUES
    # -------------------------------
    if 'benefits' not in user_input:
        user_input['benefits'] = 15000

    if 'discountprice' not in user_input:
        user_input['discountprice'] = 50000

    # -------------------------------
    # 1. USER INPUT TO DATAFRAME
    # -------------------------------
    input_df = pd.DataFrame([user_input])

    # -------------------------------
    # 2. APPLY SAME PREPROCESSING
    # -------------------------------
    processed_df = preprocess_data(input_df, training=False)

    # -------------------------------
    # 3. APPLY SAME FEATURE ENGINEERING
    # -------------------------------
    final_df = feature_engineering(processed_df, training=False)

    # -------------------------------
    # 4. REMOVE PRICE COLUMN IF PRESENT
    # -------------------------------
    if 'price' in final_df.columns:
        final_df = final_df.drop(columns=['price'])

    # -------------------------------
    # 5. ADD MISSING TRAINED COLUMNS
    # -------------------------------
    for col in feature_columns:
        if col not in final_df.columns:
            final_df[col] = 0

    # -------------------------------
    # 6. EXACT COLUMN ALIGNMENT
    # -------------------------------
    final_df = final_df[feature_columns]

    # -------------------------------
    # 7. MODEL PREDICTION
    # -------------------------------
    prediction = model.predict(final_df)[0]

    return round(float(prediction), 2)