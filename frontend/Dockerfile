# Use official lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the frontend files into the container
COPY . /app

# Install dependencies from package.json if using Node (optional)
# Otherwise, install Streamlit and Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app/main.py"]
