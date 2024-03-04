# Image
FROM python:3.11-slim

# Environment variable
ENV PYTHONUNBUFFERED 1

# Working directory of the app
WORKDIR /app

# Copy host's requirements
COPY requirements.txt ./requirements.txt

# Create virtual environment
RUN python -m venv /venv

# Install requirements within the virtual environment
RUN /venv/bin/pip install -r requirements.txt

# Try different working directories to locate uvicorn (choose the appropriate one)
WORKDIR /venv  # Start with the virtual environment directory
# WORKDIR /venv/bin  # If uvicorn is in the virtual environment's bin directory
# WORKDIR /app  # If the virtual environment is activated before copying files

# Copy application files
COPY main.py api_functions.py ./

# Expose port (optional)
EXPOSE 8000

# Entry point command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




