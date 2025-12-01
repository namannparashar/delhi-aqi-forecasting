import pytest
import json
from unittest.mock import patch, mock_open
from training.utils import load_previous_rmse

# First Test: File Does Not Exist
@patch("training.utils.os.path.exists")
def test_load_rmse_no_file(mock_exists):
    mock_exists.return_value = False
    result = load_previous_rmse()
    assert result is None 

# Second Test: File Exists with Valid Data
@patch("training.utils.os.path.exists")
def test_load_rmse_success(mock_exists):
    mock_exists.return_value = True
    
    # Last RMSE value in the mock data is 0.85
    mock_data = json.dumps([
        {"rmse": 0.95, "timestamp": "2024-01-01"}, 
        {"rmse": 0.85, "timestamp": "2024-01-02"}
    ])
    
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_previous_rmse()
        assert result == 0.85 