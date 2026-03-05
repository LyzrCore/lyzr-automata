# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a non-root user and take ownership of the app directory
RUN addgroup --system appgroup \
	&& adduser --system --ingroup appgroup appuser \
	&& chown -R appuser:appgroup /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8005 available to the world outside this container
EXPOSE 8005

# Run as non-root user
USER appuser

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]