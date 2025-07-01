import subprocess
import psutil
import time
import pandas as pd
import wmi

# Setup OpenHardwareMonitor WMI
w = wmi.WMI(namespace="root\OpenHardwareMonitor")

# -----------------------------
# 1️⃣ Clean Hadoop output path
# -----------------------------
subprocess.run(
    ["hdfs", "dfs", "-rm", "-r", "/user/hadoop/output"],
    shell=True
)

# -----------------------------
# 2️⃣ Start Hadoop MapReduce job
# -----------------------------
cmd = [
    "hadoop", "jar",
    r"C:\hadoop\share\hadoop\tools\lib\hadoop-streaming-3.2.4.jar",
    "-file", "mapper.py",
    "-mapper", "python mapper.py",
    "-file", "reducer.py",
    "-reducer", "python reducer.py",
    "-input", "/user/hadoop/input/cropdata.csv",
    "-output", "/user/hadoop/output"
]

process = subprocess.Popen(cmd, shell=True)

print("Monitoring CPU, Memory, Disk, Temp while Hadoop runs...")

# -----------------------------
# 3️⃣ Start monitoring loop
# -----------------------------
timestamps = []
cpu_usages = []
mem_usages = []
disk_usages = []
cpu_temps = []

start_time = time.time()

while process.poll() is None:
    elapsed = time.time() - start_time

    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # Get CPU temp from OpenHardwareMonitor
    cpu_temp = None
    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        if sensor.SensorType == u'Temperature' and 'CPU Package' in sensor.Name:
            cpu_temp = sensor.Value
            break

    if cpu_temp is None:
        cpu_temp = 0  # fallback

    print(f"[{elapsed:.1f}s] CPU: {cpu}%, Mem: {mem}%, Disk: {disk}%, CPU Temp: {cpu_temp}°C")

    timestamps.append(elapsed)
    cpu_usages.append(cpu)
    mem_usages.append(mem)
    disk_usages.append(disk)
    cpu_temps.append(cpu_temp)

print("✅ Hadoop MapReduce job finished!")

# -----------------------------
# 4️⃣ Save to CSV
# -----------------------------
df = pd.DataFrame({
    "time_sec": timestamps,
    "cpu_percent": cpu_usages,
    "mem_percent": mem_usages,
    "disk_percent": disk_usages,
    "cpu_temp_C": cpu_temps
})

df.to_csv("real_system_usage.csv", index=False)
print("✅ Saved real_system_usage.csv")
