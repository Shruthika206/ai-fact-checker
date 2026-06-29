FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port for Streamlit
EXPOSE 8000

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "AgentWeb.py", "--server.port=8000", "--server.address=0.0.0.0"]
