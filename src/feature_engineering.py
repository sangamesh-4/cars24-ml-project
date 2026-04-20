import pandas as pd
import numpy as np

def feature_engineering(df):

    df = df.copy()

    # Analysis
    corr = df.corr()['price'].sort_values(ascending=False)

    print("\n🔹 Top correlated features with price:")
    print(corr.head(10))

    # Feature creation
    if 'year' in df.columns:
        df['car_age'] = 2025 - df['year']

    if 'kilometerdriven' in df.columns and 'year' in df.columns:
        df['km_per_year'] = df['kilometerdriven'] / (df['car_age'] + 1)

    if 'kilometerdriven' in df.columns:
        df['log_km'] = np.log1p(df['kilometerdriven'])

    return df