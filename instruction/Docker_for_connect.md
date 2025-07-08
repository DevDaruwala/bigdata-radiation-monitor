# 📘 PyFlink Runner Usage Guide

This README provides **step-by-step instructions** for running a Flink job using Docker Compose. This setup allows you to stream data from Kafka to a PyFlink job in a portable, reproducible environment — without worrying about local Java/PyFlink/Kafka compatibility issues.

---

## 🔧 Prerequisites

Before you begin:

* Ensure Docker and Docker Compose are installed on your system.
* Clone this repository:

```bash
git clone https://github.com/DevDaruwala/bigdata-radiation-monitor.git
cd bigdata-radiation-monitor
```

---

## 🚀 Step-by-Step: Run Flink with Kafka using Docker Compose

### Step 1: Build Docker Containers

If this is your first time running the project, build all containers (especially `pyflink-runner`) with:

```bash
docker compose build --no-cache
```

This ensures Java, Python, and dependencies are correctly installed.

---

### Step 2: Start Kafka and Zookeeper

Start Kafka and Zookeeper services in the background:

```bash
docker compose up -d kafka zookeeper
```

Wait a few seconds until they are ready.

---

### Step 3: Run the PyFlink Job

Launch the PyFlink job inside the container:

```bash
docker compose up pyflink-runner
```

This will execute the Python file `flink/dummy_job.py`, which internally uses `flink_connect.py` to consume data from the Kafka topic.

> ✅ Tip: Make sure the topic name matches the one your Kafka producer is writing to.

---

### Step 4: Run the Kafka Producer (Optional)

If you want to test data streaming:

```bash
source activate radiation-cpu39  # or use your Python environment
python producer/continent_producer.py
```

This will send data to the Kafka topic your Flink job listens to.

---

## 🧪 Verifying It Works

* You should see logs from the Flink container processing incoming Kafka messages.
* Add `print()` or logging inside `dummy_job.py` to debug outputs.

---

## 🔁 Rebuild or Restart

If you change any code or dependencies:

```bash
docker compose build --no-cache
```

Then re-run:

```bash
docker compose up pyflink-runner
```

---

## 🔗 Why This Helps

Using this Docker setup ensures:

* **No local config issues** with Java, Flink, or Kafka.
* **Easy sharing** across teammates.
* **Fast recovery** from environment corruption.

---

## 🧑‍🤝‍🧑 How Teammates Can Use This

Just clone the repo and run:

```bash
docker compose build --no-cache
```

Then:

```bash
docker compose up -d kafka zookeeper
```

And finally:

```bash
docker compose up pyflink-runner
```

They don't need to install Java, PyFlink, or even configure the job — it just works.

---

For any issues, check the logs or reach out to the project maintainer.

Happy streaming! 🌊
