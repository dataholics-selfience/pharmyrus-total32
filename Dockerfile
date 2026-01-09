FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .
COPY google_patents_crawler.py .

# Railway uses PORT env variable
ENV PORT=8000

# Run with PORT from environment
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
