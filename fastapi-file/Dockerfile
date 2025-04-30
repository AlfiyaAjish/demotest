FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose the port used in application_conf.conf
EXPOSE 8000

# Create required folders (if not mounted)
RUN mkdir -p /code/uploads /code/app_db

# Start app with Uvicorn (disable --reload in production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
