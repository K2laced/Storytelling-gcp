FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set port for Cloud Run
ENV PORT 8080

# Run Flask app
CMD ["python", "main.py"]
