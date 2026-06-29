#!/bin/bash
set -e

# Install Python dependencies
pip install --no-cache-dir --upgrade pip setuptools wheel
pip install --no-cache-dir -r requirements.txt

# Run Streamlit app
streamlit run AgentWeb.py --server.port=8000 --server.address=0.0.0.0
