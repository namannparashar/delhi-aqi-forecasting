import os
import joblib
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Import our new modules
from .config import Config
from .utils import load_previous_rmse, save_metrics
from .preprocessing import load_data, add_time_features, get_split_date
from .modeling import tune_hyperparameters, build_forecaster
from .alerts import check_and_alert

def main():
    print("--- Starting Training Pipeline ---")
    
    # 1. Load and Split Data
    df_full = load_data()
    split_date = get_split_date()
    
    df_past = df_full[df_full["ds"] <= split_date].copy().reset_index(drop=True)
    df_future = df_full[df_full["ds"] > split_date].copy().reset_index(drop=True)

    # 2. Feature Engineering
    exog_cols = [c for c in df_past.columns if c not in ["unique_id", "ds", "y"]]
    df_past = add_time_features(df_past)
    all_features = exog_cols + ["day", "month", "weekday", "weekend"]

    # 3. Hyperparameter Tuning
    print("Tuning hyperparameters...")
    best_params = tune_hyperparameters(df_past, all_features)
    print("Best Params:", best_params)

    # 4. Final Training & Cross Validation
    best_model = XGBRegressor(objective="reg:squarederror", random_state=Config.RANDOM_STATE, **best_params)
    fcst_final = build_forecaster(best_model)
    
    print("Running Cross-Validation...")
    cv_df = fcst_final.cross_validation(
        df_past,
        n_windows=1,
        h=Config.TEST_HORIZON,
        static_features=[]
    )

    pred_col = [c for c in cv_df.columns if c not in ["unique_id", "ds", "y", "cutoff"]][0]
    rmse_cv = np.sqrt(mean_squared_error(cv_df["y"], cv_df[pred_col]))
    mae_cv  = mean_absolute_error(cv_df["y"], cv_df[pred_col])
    
    print(f"CV RMSE: {rmse_cv:.4f} | CV MAE: {mae_cv:.4f}")

    # 5. Fit on ALL past data
    fcst_final.fit(df_past, static_features=[])

    # 6. Prepare Future Exogenous & Save CSV
    future_30 = df_future.iloc[:Config.FORECAST_HORIZON].copy()
    future_30 = add_time_features(future_30)
    X_future = future_30[["unique_id", "ds"] + all_features]
    
    os.makedirs(os.path.dirname(Config.FUTURE_DATA_PATH), exist_ok=True)
    X_future.to_csv(Config.FUTURE_DATA_PATH, index=False)

    # 7. Model Evaluation & Alerting logic
    prev_rmse = load_previous_rmse()
    if prev_rmse: print(f"Previous RMSE: {prev_rmse:.3f}")

    # Alert if model degraded
    check_and_alert(rmse_cv, prev_rmse)

    print("Updating the model on full past data and saving...")
    os.makedirs(os.path.dirname(Config.MODEL_PATH), exist_ok=True)
    joblib.dump(fcst_final, Config.MODEL_PATH)
    
    # Always save metrics history
    save_metrics(rmse_cv)
    print("Pipeline Complete.")

if __name__ == "__main__":
    main() 

