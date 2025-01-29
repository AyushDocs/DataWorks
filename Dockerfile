# Use the official lightweight Ubuntu Python image
FROM python:3.11-slim

# Prevents Python from writing .pyc files and enables unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install required dependencies and clean up unnecessary files
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     gcc \
#     g++ \
#     python3-dev \
#     libstdc++6 \
#     libgomp1 \
#     liblapack-dev \
#     gfortran \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app

# Expose the Flask default port
EXPOSE 5000

# Command to run the Flask server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]