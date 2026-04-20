import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor

from src.evaluate import evaluate_model


def train_model(df):
    """
    Advanced Training Pipeline (Clean Version)
    """

    # -------------------------------
    # 1. SPLIT FEATURES & TARGET
    # -------------------------------
    if 'price' not in df.columns:
        raise ValueError("Target column 'price' missing")

    X = df.drop('price', axis=1)
    y = df['price']

    # -------------------------------
    # 2. TRAIN-TEST SPLIT
    # -------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # -------------------------------
    # 3. SCALING (ONLY FOR LINEAR MODELS)
    # -------------------------------
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # -------------------------------
    # 4. DEFINE MODELS
    # -------------------------------
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Lasso Regression": Lasso(alpha=0.01),

        "Random Forest": RandomForestRegressor(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        ),

        "XGBoost": XGBRegressor(
            n_estimators=400,
            learning_rate=0.03,
            max_depth=5,
            subsample=0.9,
            colsample_bytree=0.7,
            gamma=0.2,
            random_state=42,
            n_jobs=-1
        )
    }

    results = []
    trained_models = {}

    linear_models = ["Linear Regression", "Ridge Regression", "Lasso Regression"]

    # -------------------------------
    # 5. TRAIN & EVALUATE
    # -------------------------------
    for name, model in models.items():

        print(f"\n🔹 Training {name}...")

        # -------------------------------
        # TRAINING
        # -------------------------------
        if name in linear_models:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)

            cv_scores = cross_val_score(
                model, X_train_scaled, y_train, cv=5, scoring='r2'
            )

        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            cv_scores = cross_val_score(
                model, X_train, y_train, cv=5, scoring='r2'
            )

        # -------------------------------
        # EVALUATION
        # -------------------------------
        metrics = evaluate_model(y_test, y_pred, name)

        metrics['CV Mean'] = round(np.mean(cv_scores), 4)
        metrics['CV Std'] = round(np.std(cv_scores), 4)

        results.append(metrics)
        trained_models[name] = model

    # -------------------------------
    # 6. RESULTS TABLE
    # -------------------------------
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="R2 Score", ascending=False)

    return results_df, trained_models