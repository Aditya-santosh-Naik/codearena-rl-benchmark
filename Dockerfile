FROM python:3.10-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Required for HF Spaces: Expose default port 7860
EXPOSE 7860

# FastAPI server running on 0.0.0.0
CMD ["uvicorn", "server.env:app", "--host", "0.0.0.0", "--port", "7860"]
