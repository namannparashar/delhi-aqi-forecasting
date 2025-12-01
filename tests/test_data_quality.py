import pytest 
import pandas as pd
import os
from training.config import Config

@pytest.fixture(scope="module")
def data():
    # Check if data file exists
    path = Config.DATA_PATH
    if not os.path.exists(path):
        pytest.skip(f"Data file not found at {path}. Run fetch_data first.")
    
    # Read CSV
    df = pd.read_csv(path)
    
    # Standardize column names (strip spaces)
    df.columns = [c.strip() for c in df.columns]
    return df

def test_columns_present(data):
    required_columns = ["date", "PM2_5", "Wind_Speed", "Temperature", "Humidity","Wind_Direction"]
    for col in required_columns:
        assert col in data.columns, f"Missing required column: {col}"

def test_no_missing_values(data):
    assert not data.isnull().values.any(), "Data contains missing values"

def test_date_format(data):
    try:
        pd.to_datetime(data["date"])
    except Exception as e:
        pytest.fail(f"Date column has invalid format: {e}")

def test_value_ranges(data):
    assert data["PM2_5"].between(0, 1000).all(), "PM2_5 values out of range"
    assert data["Wind_Speed"].between(0, 400).all(), "Wind_Speed values out of range"
    assert data["Temperature"].between(-50, 60).all(), "Temperature values out of range"
    assert data["Humidity"].between(0, 100).all(), "Humidity values out of range"
    assert data["Wind_Direction"].between(0, 360).all(), "Wind_Direction values out of range"