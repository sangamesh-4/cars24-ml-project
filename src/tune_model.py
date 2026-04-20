import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from xgboost import XGBRegressor


def tune_xgboost(df):
    """
    Hyperparameter tuning for XGBoost using RandomizedSearchCV
    """

    # -------------------------------
    # 1. SPLIT DATA
    # -------------------------------
    X = df.drop('price', axis=1)
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # -------------------------------
    # 2. DEFINE MODEL
    # -------------------------------
    model = XGBRegressor(random_state=42, n_jobs=-1)

    # -------------------------------
    # 3. PARAMETER GRID
    # -------------------------------
    param_dist = {
        "n_estimators": [200, 300, 500, 700],
        "learning_rate": [0.01, 0.03, 0.05, 0.1],
        "max_depth": [3, 4, 5, 6, 7],
        "subsample": [0.6, 0.7, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.7, 0.8, 1.0],
        "gamma": [0, 0.1, 0.2, 0.3]
    }

    # -------------------------------
    # 4. RANDOM SEARCH
    # -------------------------------
    random_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_dist,
        n_iter=25,                # try 25 combinations
        scoring='r2',
        cv=3,
        verbose=1,
        random_state=42,
        n_jobs=-1
    )

    random_search.fit(X_train, y_train)

    # -------------------------------
    # 5. BEST MODEL
    # -------------------------------
    best_model = random_search.best_estimator_

    print("\n🔥 Best Parameters:")
    print(random_search.best_params_)

    # -------------------------------
    # 6. EVALUATE
    # -------------------------------
    r2 = best_model.score(X_test, y_test)

    print("\n✅ Tuned Model R2:", round(r2, 4))

    return best_model