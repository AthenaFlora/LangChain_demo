FROM python:3.10-slim

# Set working directory
WORKDIR /workspace

# install wkhtmltopdf for pdfkit
RUN apt update && apt install -y wkhtmltopdf

# Install requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]