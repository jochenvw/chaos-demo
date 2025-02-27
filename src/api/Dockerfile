# Use Python slim image for a smaller footprint
FROM python:3.9-slim

# Install shell utilities
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]