# Base Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files into container
COPY . /app

# Install system dependencies and pip packages
RUN apt-get update && \
    apt-get install -y python3-pip build-essential && \
    pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI (Railway or Render will provide $PORT)
ENV PORT 8000

# Command to start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
