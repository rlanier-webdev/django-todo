# Stage 1: Build Stage
# Use an official Python image as the base
FROM python:3.13-slim as builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Production Stage (for smaller image size)
FROM python:3.13-slim

# Create a non-root user for security (optional but recommended)
RUN adduser --system --group appuser
USER appuser

# Set the working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
# Copy the application code
COPY --chown=appuser:appuser . .

# Expose the port Gunicorn will run on
EXPOSE 8000

# Command to run the application using Gunicorn
# Replace 'your_project_name.wsgi' with your actual project's WSGI file path
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]