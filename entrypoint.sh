#!/bin/bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "Waiting for API to start..."
sleep 15

streamlit run dashboard/streamlit_app.py --server.port 7860 --server.address 0.0.0.0 