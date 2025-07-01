from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

spark = SparkSession.builder.appName("CropYield").getOrCreate()

df = spark.read.csv("cropdata.csv", header=True, inferSchema=True)

# Group by State and get total yield
result = df.groupBy("State").agg(sum("Yield").alias("Total_Yield"))

result.show()
