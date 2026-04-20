import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split


def plot_all(results, models, df_final):
    """
    Complete visualization pipeline
    """

    # -------------------------------
    # 1. DATA PREP
    # -------------------------------
    X = df_final.drop('price', axis=1)
    y = df_final['price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = models['XGBoost']
    y_pred = model.predict(X_test)

    # -------------------------------
    # 2. MODEL COMPARISON
    # -------------------------------
    fig1 = px.bar(
        results,
        x='Model',
        y='R2 Score',
        title='Model Comparison (R²)',
        text='R2 Score'
    )
    fig1.show()

    # -------------------------------
    # 3. MULTI METRIC
    # -------------------------------
    fig2 = px.bar(
        results,
        x='Model',
        y=['R2 Score', 'RMSE', 'MAE'],
        barmode='group',
        title='Model Performance'
    )
    fig2.show()

    # -------------------------------
    # 4. ACTUAL VS PREDICTED
    # -------------------------------
    fig3 = px.scatter(
        x=y_test,
        y=y_pred,
        labels={'x':'Actual', 'y':'Predicted'},
        title='Actual vs Predicted'
    )

    fig3.add_shape(
        type='line',
        x0=y_test.min(), y0=y_test.min(),
        x1=y_test.max(), y1=y_test.max(),
        line=dict(dash='dash')
    )

    fig3.show()

    # -------------------------------
    # 5. RESIDUAL PLOT
    # -------------------------------
    residuals = y_test - y_pred

    fig4 = px.scatter(
        x=y_pred,
        y=residuals,
        labels={'x':'Predicted', 'y':'Residual'},
        title='Residual Plot'
    )

    fig4.add_hline(y=0, line_dash='dash')
    fig4.show()

    # -------------------------------
    # 6. RESIDUAL DISTRIBUTION
    # -------------------------------
    fig5 = px.histogram(
        residuals,
        nbins=50,
        title='Residual Distribution'
    )
    fig5.show()

