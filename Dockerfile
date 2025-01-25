# Use the official Python image as the base image
FROM python:3.12.7-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the Flask default port
EXPOSE 5000

# Command to run the Flask server
CMD ["python", "server.py"]
