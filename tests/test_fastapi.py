import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

# Create a test client
client = TestClient(app)

# --- FIXTURES (Dummy Data) ---

@pytest.fixture
def mock_x_future():
    # Simulate the future exogenous dataframe.
    return pd.DataFrame({
        "unique_id": ["air_quality", "air_quality"],
        "ds": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "exog_1": [10, 20]
    }) 


def test_forecast_not_initialized():
    # Patch with an empty dictionary (simulating failure to load)
    with patch("app.main.models", {}):
        response = client.get("/forecast")
        
        assert response.status_code == 500
        assert response.json()["detail"] == "Model not initialized"


def test_forecast_prediction_crash(mock_x_future):
    # Mock model that raises an error when predict is called
    bad_model = MagicMock()
    bad_model.predict.side_effect = ValueError("Input contains NaN")
    
    fake_models_storage = {
        "fcst_model": bad_model,
        "X_future": mock_x_future,
        "current_data": pd.DataFrame()
    }
    
    with patch("app.main.models", fake_models_storage):
        response = client.get("/forecast")
        
        assert response.status_code == 500
        # Ensure the error message bubbles up to the response
        assert "Input contains NaN" in response.json()["detail"] 