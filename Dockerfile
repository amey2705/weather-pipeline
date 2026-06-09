FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies first (faster rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project code
COPY ingestion/ ./ingestion/
COPY transformation/ ./transformation/

# Tell Python to treat folders as modules
ENV PYTHONPATH=/app

# Default command to run when container starts
CMD ["python", "-m", "ingestion.fetch_weather"]
