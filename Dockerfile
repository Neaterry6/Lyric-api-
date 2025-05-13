# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the full app AFTER dependencies
COPY . /app/

# Expose Flask port
EXPOSE 5000

# ✅ Fix Gunicorn startup command
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
