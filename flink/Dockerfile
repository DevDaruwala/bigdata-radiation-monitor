FROM flink:1.18

USER root

RUN apt-get update && \
    apt-get install -y python3 netcat-openbsd python3-pip curl && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install apache-flink==1.18.1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY jars/*.jar /opt/flink/connectors/
COPY src /app/src
COPY wait-for-kafka.sh /app/wait-for-kafka.sh
RUN chmod +x /app/wait-for-kafka.sh

WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"
