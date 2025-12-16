FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file (if it exists) or install Flask directly
COPY requirements.txt* /app/

RUN if [ -f requirements.txt ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    else \
      pip install --no-cache-dir flask; \
    fi

# Copy application code
COPY app.py /app/

EXPOSE 5000

CMD ["python3", "app.py"]
