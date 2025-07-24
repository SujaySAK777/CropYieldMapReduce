# 🌾 CropYieldMapReduce — Big Data Crop Analysis & Prediction

**CropYieldMapReduce** is a practical mini-project that demonstrates Big Data processing in agriculture using:

- 📈 **Apache Hadoop MapReduce** for analyzing crop land utilization metrics.
- ⚡ **Apache Spark MLlib** for predicting average crop yield based on input factors.
- 🗂️ **Streamlit Web App** for an interactive user interface.
- 🔥 **System Monitoring** to observe CPU, Memory, Disk usage & approximate heat generation while running heavy tasks.

This project is useful for understanding Big Data pipelines, parallel processing, and how real-world datasets can be handled and visualized efficiently.

---

## 🧩 Key Highlights

✅ Data visualization for crop & land utilization\
✅ MLlib-based crop yield prediction\
✅ Hadoop MapReduce with CPU/Memory/Temperature monitoring\
✅ One-click web app built with Streamlit\
✅ Simple to clone & run on Windows

---

## ⚙️ Software Requirements

Before you begin, make sure you have installed:

- **Python** (3.10 or higher) — for Streamlit, pandas, and scripts.
- **Java JDK** (version 8 or higher) — required by Hadoop and Spark.
- **Hadoop** (3.x) — for running MapReduce tasks.
- **Apache Spark** (3.5.5 recommended) — for MLlib-based predictions.
- **Streamlit** — to run the web app interface.
- **psutil** — Python library for monitoring system resources.
- **pywin32** and **wmi** — for reading CPU temperature through OpenHardwareMonitor.
- **OpenHardwareMonitor** — must be running to expose CPU temperature sensors via WMI.

---

## 📥 **How to Clone the Repository**

```bash
git clone https://github.com/SujaySAK777/CropYieldMapReduce.git
cd CropYieldMapReduce
```

---

## 🐍 **Python Environment Setup**

**1️⃣ Create a Virtual Environment**

```bash
python -m venv venv
```

**2️⃣ Activate the Environment**

```bash
# Windows
venv\Scripts\activate
```

**3️⃣ Install Python Dependencies**

First, create a `requirements.txt` file with:

```
streamlit
pandas
plotly
scikit-learn
psutil
pyspark
pywin32
wmi
```

Then install all packages:

```bash
pip install -r requirements.txt
```

---

## 🗄️ **Hadoop Setup**

1️⃣ Download Hadoop (prebuilt binaries) and extract it.\
2️⃣ Configure `HADOOP_HOME` and `JAVA_HOME` in your environment variables.\
3️⃣ Format the NameNode:

```bash
hdfs namenode -format
```

4️⃣ Start Hadoop services:

```bash
start-dfs.cmd
start-yarn.cmd
```

5️⃣ Place your input data into HDFS:

```bash
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put cropdata.csv /user/hadoop/input/
```

---

## ⚡ **Spark Setup**

1️⃣ Download Spark with Hadoop bundled.\
2️⃣ Add `SPARK_HOME` to your PATH or run `spark-submit` using its full path.\
3️⃣ Confirm it’s working:

```bash
spark-submit --version
```

---

## 🔥 **Heat & Resource Monitoring Setup**

- Download and run **OpenHardwareMonitor** on your machine.
- Launch `OpenHardwareMonitor.exe` **before** running the monitoring script to expose hardware sensors.
- The Python monitoring script (`monitor_hadoop.py`) uses `psutil` for CPU, RAM, Disk and `wmi` to get CPU temperature via OpenHardwareMonitor’s WMI namespace.

---

## 🚀 **How to Run**

### ✅ 1️⃣ **Launch the Streamlit Web App**

Run:

```bash
streamlit run main.py
```

Your browser will open with 3 sections:

**a) Spark MLlib Prediction**

- Select State & Crop (loaded dynamically from your dataset).
- Input values: area, agri land, barren land, rainfall, fertilizer, pesticide.
- Click **Predict** → This runs `spark_easy_web.py` using `spark-submit` and shows the predicted yield.

**b) Visualization Dashboard**

- Explore plots and trends from `crop_analysis_output.csv`.
- See state-wise land use, barren land %, yield trends, and more.

**c) Hadoop Resource Monitoring**

- Click **Run MapReduce & Monitor**.
- Runs the Hadoop Streaming job (`mapper.py` + `reducer.py`).
- Simultaneously logs CPU %, Memory %, Disk usage %, and CPU Temp (if OpenHardwareMonitor is running).
- Shows 4 separate time-series charts for system usage.

---

## 🔧 **How Heat Monitoring Works**

- The `monitor_hadoop.py` script starts the MapReduce job.
- Uses `psutil` for CPU, RAM, Disk.
- Uses `wmi` to read CPU temperature from OpenHardwareMonitor.
- Logs all metrics every second to `real_system_usage.csv`.
- The Streamlit dashboard displays graphs for each metric under **Hadoop Resource Monitoring**.

---

## 🗃️ **How MapReduce Works**

- **Mapper:** Reads each row, extracts needed columns: State, Crop, Area, Yield, Agri Land, Barren Land, Rainfall, Fertilizer, Pesticide.
- **Reducer:** Groups by (State, Crop) → computes average values per group.
- **Output:** Shows average agri land, barren land, yield, rainfall, and fertilizer/pesticide use per hectare.

---

## 💡 **Key Benefits**

✅ Learn how big data splits and parallelizes tasks with Hadoop MapReduce.\
✅ See how Spark’s MLlib can learn from past data to predict future yields.\
✅ Visualize the resource footprint of big data tasks — CPU, memory, disk, and approximate heat.\
✅ No complex manual commands — run everything through a single Streamlit app.

---

## ⚠️ **Important Notes**

- Always launch **OpenHardwareMonitor** first to make CPU temperature available.
- If your `spark-submit` is not in PATH, update `main.py` with the full absolute path to `spark-submit.cmd`.
- Make sure your CSV (`crop_analysis_output.csv`) covers all States & Crops you want to select.

---

## 🎉 **Done!**

✅ You’re ready to clone, run, explore, and learn from your very own Big Data mini-project.\
Open an issue or pull request on your GitHub if you improve it!

