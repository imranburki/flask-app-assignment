# Use official Python slim image as base
FROM python:3.11-slim AS builder

# Set working directory inside container
WORKDIR /app

# Copy only required files first (to leverage Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Use a lightweight runtime image for the final build
FROM python:3.11-slim

# Set a non-root user for security
RUN useradd -m appuser
USER appuser

# Set working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files
COPY . .

# Expose port 5000
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
