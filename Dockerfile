# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Install iperf3
RUN apt-get update && apt-get install -y iperf3 iputils-ping && apt-get clean

# Copy project
COPY . /code/

# Expose the port the app runs on
EXPOSE 8060

# Command to run the application
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:80", "--timeout", "120", "wsgi:app"]
