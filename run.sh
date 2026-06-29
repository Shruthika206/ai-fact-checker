#!/bin/bash

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Run Streamlit app
streamlit run AgentWeb.py \
  --server.port=8000 \
  --server.address=0.0.0.0 \
  --logger.level=info