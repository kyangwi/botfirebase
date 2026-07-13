# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install system dependencies needed for compiling ChromaDB and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files for WhiteNoise
RUN python manage.py collectstatic --noinput

# Run the app on the specified port
CMD python manage.py migrate --noinput && exec gunicorn sqlchat_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0

