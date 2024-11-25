# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application's port (adjust based on your app, e.g., 8000 for FastAPI)
EXPOSE 5002

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002"]