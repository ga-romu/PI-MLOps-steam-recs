# Image
FROM python:3.11-slim

# working directory ofthe app
WORKDIR /app

# Copy host's requirements
COPY requirements.txt ./requirements.txt

# Install requirements
RUN pip install -r requirements.txt

# Copy github
COPY main.py api_functions.py ./  /app/

# Entry point command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]