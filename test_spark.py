import os
from pyspark.sql import SparkSession

os.environ["PYSPARK_PYTHON"] = r"C:\Users\Dell\AppData\Local\Programs\Python\Python310\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\Dell\AppData\Local\Programs\Python\Python310\python.exe"

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Test") \
    .getOrCreate()

print("Spark Session created successfully")

# Your actual Spark logic here...

spark.stop()
