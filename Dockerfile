FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create database directory
RUN mkdir -p /app/database

# Expose Streamlit port (informational)
EXPOSE 8501

# Health check uses the PORT env var (fallback to 8501)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl --fail "http://localhost:${PORT:-8501}/_stcore/health" || exit 1

# Run Streamlit binding to the PORT env var Render provides (fallback to 8501 locally)
CMD ["bash", "-lc", "exec streamlit run Home.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true"]
