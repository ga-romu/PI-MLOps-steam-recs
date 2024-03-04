# Image
FROM python:3.11.7

# Working directory of the app
WORKDIR /app

# Copy host's requirements
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Entry point command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




