#fetch_data.py

# importing necessary libraries
from google.cloud import bigquery
import pandas as pd
from datetime import datetime
import os

# Function to load SQL query from a file
def load_sql(path):
    with open(path, "r") as f:
        return f.read()

def get_data_from_bigquery():
    # Initialize a BigQuery client
    client = bigquery.Client()

    # Load and execute the SQL query for latest air quality data and current data
    sql_query = load_sql("sql/air_quality_bq.sql")
    df = client.query(sql_query).to_dataframe()
    os.makedirs("data", exist_ok=True)
    latest_path = "data/air_quality_latest.csv"
    df.to_csv(latest_path, index=False)

    sql_query_current = load_sql("sql/actual_data.sql")
    df_current = client.query(sql_query_current).to_dataframe()
    latest_path_actual = "data/air_quality_current.csv"
    df_current.to_csv(latest_path_actual, index=False) 

    print("✅ Data pulled from BigQuery")
    print("   Data Till Current Date    :", latest_path_actual) 
    print("   Latest Data               :", latest_path)

if __name__ == "__main__":
    get_data_from_bigquery() 
