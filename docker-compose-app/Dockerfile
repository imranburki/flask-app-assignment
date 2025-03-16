# Stage 1: Builder - Install dependencies
FROM python:3.11-slim AS builder

# Set working directory inside container
WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime - Use a lightweight Python image
FROM python:3.11-slim

# Set a non-root user for security
RUN useradd -m appuser
USER appuser

# Set working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy application files
COPY . .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
# Run Flask app using Hypercorn
CMD ["hypercorn", "app:asgi_app", "--bind", "0.0.0.0:5000"]

# Run Flask app
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

