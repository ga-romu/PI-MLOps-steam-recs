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

# Working directory within the virtual environment
WORKDIR /venv/lib/python3.11/site-packages 

# Copy application files
COPY main.py api_functions.py ./

# Entry point command
CMD ["uvicorn", "main:app"]



