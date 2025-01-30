# Use the official lightweight Ubuntu Python image
FROM python:3.11-slim

# Prevents Python from writing .pyc files and enables unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app



# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g prettier && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
# Copy the application code into the container
ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=${GITHUB_TOKEN} 
RUN git config --global user.email "ayushalokdubey@gmail.com"
RUN git config --global user.name "AyushDocs"

COPY . /app

# Expose the Flask default port
EXPOSE 8000

# Command to run the Flask server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]