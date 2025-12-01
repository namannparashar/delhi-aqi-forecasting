import os 
import pandas as pd
from datetime import datetime
from .config import Config

def load_data():
    if not os.path.exists(Config.DATA_PATH):
        raise FileNotFoundError(f"{Config.DATA_PATH} not found.")
    
    df = pd.read_csv(Config.DATA_PATH)
    df.columns = [c.strip() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").rename(columns={"date": "ds", "PM2_5": "y"})
    df["unique_id"] = "air_quality"
    return df.sort_values("ds").reset_index(drop=True)

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['day'] = df['ds'].dt.day
    df['month'] = df['ds'].dt.month
    df['weekday'] = df['ds'].dt.weekday
    df['weekend'] = df['weekday'].isin([5, 6]).astype(int)
    return df

def get_split_date():
    # Define cut-off as yesterday
    return pd.Timestamp(datetime.now()) - pd.Timedelta(days=1)