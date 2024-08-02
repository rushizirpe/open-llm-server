# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /data

# Copy the current directory contents into the container at /data
COPY . /data

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8888

# Command to run the app
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8888"]
