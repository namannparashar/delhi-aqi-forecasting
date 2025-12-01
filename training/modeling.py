import optuna
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from mlforecast import MLForecast
from mlforecast.lag_transforms import RollingMean, RollingStd, RollingMax
from .config import Config

def build_forecaster(model) -> MLForecast:
    return MLForecast(
        models=[model],
        freq='D',
        lags=[1, 2, 3, 7, 14, 28],
        lag_transforms={
            7:  [RollingMean(7),  RollingStd(7)],
            14: [RollingMean(14)],
            28: [RollingMean(28), RollingMax(28)],
        },
    )

def tune_hyperparameters(df_past, all_features):
    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 200, 1200),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "objective": "reg:squarederror",
            "random_state": Config.RANDOM_STATE,
        }

        model = XGBRegressor(**params)
        fcst = build_forecaster(model)

        train_df = df_past.iloc[:-Config.TEST_HORIZON].copy() 
        val_df   = df_past.iloc[-Config.TEST_HORIZON:].copy()

        fcst.fit(train_df, static_features=[])
        
        X_val = val_df[["unique_id", "ds"] + all_features]
        preds = fcst.predict(h=Config.TEST_HORIZON, X_df=X_val)

        merged = val_df[["ds", "y"]].merge(preds, on="ds")
        return np.sqrt(mean_squared_error(merged["y"], merged["XGBRegressor"]))

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=Config.N_TRIALS)
    return study.best_params 