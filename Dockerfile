# Dockerfile

# --- Stage 1: Build ---
# Use an official Python runtime as a parent image
FROM python:3.9-slim as builder

# Set the working directory in the container
WORKDIR /usr/src/app


# Copy the requirements file into the container
COPY requirements.txt ./

# Install Python dependencies

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./app ./app

# --- Stage 2: Runtime ---
#  Use a slim Python image for the runtime stage to reduce image size 
FROM python:3.9-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code from the builder stage
COPY --from=builder /usr/src/app/app ./app

#  Make port 8080 available to the world outside this container 
EXPOSE 8080

# Define environment variable to ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

# Command to run the application using Uvicorn

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]