# Use official Python 3.12 image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first for faster caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose port 10000
EXPOSE 10000

# Start the app using gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:10000"]