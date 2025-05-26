FROM python:3.10-slim

# Set working directory
WORKDIR /workspace

# Install requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]