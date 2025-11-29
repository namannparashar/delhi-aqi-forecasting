from google.cloud import bigquery
import pandas as pd
from datetime import datetime
import os

def load_sql(path):
    with open(path, "r") as f:
        return f.read()

def get_data_from_bigquery():
    client = bigquery.Client()

    # Load SQL from file
    sql_query = load_sql("sql/air_quality_bq.sql")

    df = client.query(sql_query).to_dataframe()

    # Prepare folder
    os.makedirs("data", exist_ok=True)

    # Timestamped snapshot
    ts_str = datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")
    versioned_path = f"data/air_quality_{ts_str}.csv"
    df.to_csv(versioned_path, index=False)

    # Latest alias
    latest_path = "data/air_quality_latest.csv"
    df.to_csv(latest_path, index=False)

    print("✅ Data pulled from BigQuery")
    print("   Versioned snapshot:", versioned_path)
    print("   Latest alias     :", latest_path)

if __name__ == "__main__":
    get_data_from_bigquery()
