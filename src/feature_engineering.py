import pandas as pd
import numpy as np
from datetime import datetime


def feature_engineering(df, training=True):
    """
    Feature engineering pipeline
    training=True  -> analysis mode
    training=False -> inference mode
    """

    df = df.copy()

    # -------------------------------
    # 1. ANALYSIS ONLY DURING TRAINING
    # -------------------------------
    if training and 'price' in df.columns:
        corr = df.corr()['price'].sort_values(ascending=False)

        print("\n🔹 Top correlated features with price:")
        print(corr.head(10))

    # -------------------------------
    # 2. FEATURE CREATION
    # -------------------------------
    current_year = datetime.now().year

    if 'year' in df.columns:
        df['car_age'] = current_year - df['year']

    if 'kilometerdriven' in df.columns and 'car_age' in df.columns:
        df['km_per_year'] = df['kilometerdriven'] / (df['car_age'] + 1)

    if 'kilometerdriven' in df.columns:
        df['log_km'] = np.log1p(df['kilometerdriven'])

    return df