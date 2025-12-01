import os
import json
from datetime import datetime
from .config import Config

def load_previous_rmse():
    if not os.path.exists(Config.METRICS_PATH):
        return None
    try:
        with open(Config.METRICS_PATH, "r") as f:
            content = f.read()
            if not content: return None
            data = json.loads(content)
        
        if isinstance(data, list) and len(data) > 0:
            return data[-1].get("rmse")
        return None
    except (json.JSONDecodeError, IndexError, AttributeError):
        return None

def save_metrics(rmse: float):
    os.makedirs(os.path.dirname(Config.METRICS_PATH), exist_ok=True)
    data = []
    
    if os.path.exists(Config.METRICS_PATH):
        try:
            with open(Config.METRICS_PATH, "r") as f:
                content = f.read()
                if content:
                    loaded = json.loads(content)
                    data = loaded if isinstance(loaded, list) else [loaded]
        except json.JSONDecodeError:
            pass 

    new_entry = {
        "rmse": float(rmse),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(new_entry)
    
    with open(Config.METRICS_PATH, "w") as f:
        json.dump(data, f, indent=2)