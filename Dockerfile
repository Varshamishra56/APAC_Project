# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Expose port 8080 for the Streamlit app to run
EXPOSE 8080

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies from requirements.txt (assuming it is present in your project)
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point to run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
