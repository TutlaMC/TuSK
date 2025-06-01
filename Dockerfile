# Use an official slim Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install git and build tools (for git+ installs)
RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project into the container
COPY . .

# Run the bot from src/main.py
CMD ["python", "src/main.py"]
