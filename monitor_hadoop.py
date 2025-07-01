import subprocess
import psutil
import time
import pandas as pd

subprocess.run(
    ["hdfs", "dfs", "-rm", "-r", "/user/hadoop/output"],
    shell=True
)

# ✅ Use raw string for Windows path!
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

print("Monitoring system usage...")

cpu_log = []
mem_log = []
timestamps = []

start_time = time.time()

while process.poll() is None:
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    elapsed = time.time() - start_time

    timestamps.append(elapsed)
    cpu_log.append(cpu)
    mem_log.append(mem)

    print(f"[{elapsed:.1f} sec] CPU: {cpu}% | Memory: {mem}%")

print("✅ Hadoop MapReduce job finished!")

df = pd.DataFrame({
    "time_sec": timestamps,
    "cpu_percent": cpu_log,
    "mem_percent": mem_log
})

df.to_csv("resource_usage.csv", index=False)
print("Saved resource_usage.csv ✅")
