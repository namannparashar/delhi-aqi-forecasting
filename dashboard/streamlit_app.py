import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- CONFIGURATION & STYLE ---
st.set_page_config(page_title="Delhi PM2.5 Forecast", layout="centered")

st.markdown(
    """
    <style>
    /* Main Background - Using a Darker Grey for better contrast */
    .stApp {
        background-color: #1E1E1E; 
    }

    /* Headers - Fixed 'text-align' syntax */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        text-align: center; 
    }

    /* Standard Text */
    p, label, li, span, div {
        color: white !important;
    }

    /* Metric Values */
    div[data-testid="stMetricValue"] {
        color: white !important;
    }

    /* Metric Labels */
    div[data-testid="stMetricLabel"] {
        color: #d3d3d3 !important; /* Light grey */
    }
    
    /* Center the Metrics */
    div[data-testid="stMetric"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("-- Delhi PM2.5 Forecast Dashboard --")

# --- DATA LOADING ---
API_URL = "http://localhost:8000/forecast"

try:
    with st.spinner("Fetching latest air quality data..."):
        resp = requests.get(API_URL)

    if resp.status_code == 200:
        # Load Forecast
        data = resp.json()["forecast"]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df['Type'] = 'Forecast'

        # Load Actuals
        actual_data = resp.json()["actual_data"]
        df_actual = pd.DataFrame(actual_data)
        df_actual['date'] = pd.to_datetime(df_actual['date'])
        df_actual['Type'] = 'Actual'

        # --- METRICS ---
        current_val = df_actual['PM2_5'].iloc[-1]
        predicted_avg = df['PM2_5'].mean()
        max_forecast = df['PM2_5'].max()

        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric("Latest PM2.5", f"{current_val:.1f}", delta="Live")
        kpi2.metric("Avg Forecast (30 Days)", f"{predicted_avg:.1f}", delta_color="off")
        kpi3.metric(
            "Peak Forecast (30 Days)", 
            f"{max_forecast:.1f}",
            delta="High Pollution" if max_forecast > 60 else "Normal",
            delta_color="inverse"
        )

        st.markdown("---")
        
        # Combine: Actuals  + Forecasts
        final_df = pd.concat([df_actual, df], ignore_index=True)
        final_df = final_df.sort_values('date')

        # --- PLOTTING ---
        fig = px.line(
            final_df, 
            x="date", 
            y="PM2_5", 
            color="Type", 
            color_discrete_map={
                "Actual": "#00FF00",
                "Forecast": "white"
            }
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="rgba(255, 255, 255, 1)"),
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', title="Date"),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', title="PM2.5 Level"),
            legend=dict(orientation="h", y=1.1) # Move legend to top
        )

        
        fig.update_traces(patch={"line": {"dash": "dash"}}, selector={"legendgroup": "Forecast"})

        st.plotly_chart(fig, width="stretch", theme=None)

    else:
        st.error(f"API Error {resp.status_code}")
        st.write("Server response:", resp.text)

except Exception as e:
    print(f"DEBUG ERROR: {e}")
    st.error("Error Loading The Dashboard (Connection Failed)")