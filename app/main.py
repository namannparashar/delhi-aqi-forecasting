import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

# Import Config
from training.config import Config

# Global dictionary to hold loaded models and data
models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load model and data when the app starts.
    This prevents reloading the model on every single request (which is slow).
    """
    # Check if files exist
    if not os.path.exists(Config.MODEL_PATH):
        raise RuntimeError(f"Model not found at {Config.MODEL_PATH}. Run training first.")
    
    if not os.path.exists(Config.FUTURE_DATA_PATH):
        raise RuntimeError(f"Future exogenous data not found at {Config.FUTURE_DATA_PATH}.")
    
    if not os.path.exists(Config.CURRENT_DATA_PATH):
        raise RuntimeError(f"Current data not found at {Config.CURRENT_DATA_PATH}.")

    # Load data and model
    models["fcst_model"] = joblib.load(Config.MODEL_PATH)
    df_future = pd.read_csv(Config.FUTURE_DATA_PATH)
    df_future['ds'] = pd.to_datetime(df_future['ds']) 
    
    models["X_future"] = df_future
    
    if os.path.exists(Config.CURRENT_DATA_PATH):
        models["current_data"] = pd.read_csv(Config.CURRENT_DATA_PATH)
    else:
        models["current_data"] = pd.DataFrame() # Empty fallback
        print("Warning: Current data file not found.")

    print("✅ Model and Data Loaded Successfully")
    yield
        # Cleanup on shutdown
    models.clear()

app = FastAPI(title="Delhi PM2.5 Forecast API", lifespan=lifespan)

@app.get("/")
def root():
    return {"status": "ok", "message": "Delhi PM2.5 forecast API is live."}

@app.get("/forecast")
def get_forecast():
    """
    Returns the forecasted values and actual AQI data.
    """
    fcst_model = models.get("fcst_model")
    X_future = models.get("X_future")
    current_data = models.get("current_data")

    if not fcst_model or X_future is None:
        raise HTTPException(status_code=500, detail="Model not initialized")

    try:
        # Calculate Horizon based on loaded future data
        horizon = X_future.shape[0]

        # Generate Predictions
        preds = fcst_model.predict(h=horizon, X_df=X_future)

        # Format Forecast Data
        out = preds[['ds', 'XGBRegressor']].rename(columns={
            'ds': 'date',
            'XGBRegressor': 'PM2_5'
        })
        out['date'] = pd.to_datetime(out['date']).dt.strftime('%Y-%m-%d')
        out['PM2_5'] = out['PM2_5'].round(0).astype(int)

        # Format Actual Data
        if not current_data.empty:
            
            actuals_out = current_data.copy()
            
            if 'date' in actuals_out.columns:
                actuals_out['date'] = pd.to_datetime(actuals_out['date']).dt.strftime('%Y-%m-%d')
            actuals_dict = actuals_out.to_dict(orient='records')
        else:
            actuals_dict = []

        return {
            "horizon": horizon,
            "forecast": out.to_dict(orient='records'),
            "actual_data": actuals_dict
        }

    except Exception as e:
        print(f"Error generating forecast: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    