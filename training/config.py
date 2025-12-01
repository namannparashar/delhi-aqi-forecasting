import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Paths
    DATA_PATH = "data/air_quality_latest.csv"
    MODEL_PATH = "models/fcst_model.joblib"
    METRICS_PATH = "models/metrics.json"
    FUTURE_DATA_PATH = "models/X_future.csv"
    EXOG_PATH  = 'models/X_future.csv'
    CURRENT_DATA_PATH = 'data/air_quality_current.csv'

    # Model Params
    TEST_HORIZON = 30
    FORECAST_HORIZON = 30
    RANDOM_STATE = 42
    FACTOR = 1.1 # 10% tolerance for model degradation
    
    # Tuning
    N_TRIALS = 50

    # API Keys
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")