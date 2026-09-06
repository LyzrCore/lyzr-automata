# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Run as an unprivileged user instead of root
RUN useradd --create-home --uid 1000 jazon && chown -R jazon:jazon /app
USER jazon

# Make port 8005 available to the world outside this container
EXPOSE 8005

# Run the FastAPI app when the container launches
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8005"]
