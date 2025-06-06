FROM python:3.10

# ✅ Install Java 17 instead of Java 11 (Java 11 is missing in bookworm repos)
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean

# ✅ Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Setup working directory and code
WORKDIR /app
COPY flink/ ./flink/

# Run the job
CMD ["python", "flink/dummy_job.py"]
