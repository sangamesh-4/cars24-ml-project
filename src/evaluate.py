from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np

def evaluate_model(y_true, y_pred, model_name="Model"):
    
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    
    return {
        "Model": model_name,
        "R2 Score": round(r2, 4),
        "RMSE": round(rmse, 2),
        "MAE": round(mae, 2)
    }