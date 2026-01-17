FROM python:3.14-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY app.py .
COPY templates/ templates/

# Create data directory
RUN mkdir -p /data

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]