# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install any needed system dependencies (e.g., for certain Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# We use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
# We copy the entire project context, but.dockerignore should be used to exclude unnecessary files.
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
# This command will be executed when the container starts
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]