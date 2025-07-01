from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.regression import LinearRegression

# 1️⃣ Start Spark session
spark = SparkSession.builder \
    .appName("CropYieldPrediction_WithCrop_And_State") \
    .getOrCreate()

# 2️⃣ Load your cleaned CSV (MapReduce output)
df = spark.read.csv(
    "C:/Users/Dell/HadoopProjects/CropYieldMapReduce/crop_analysis_output.csv",
    header=True,
    inferSchema=True
)

print("Initial dataset:")
df.show(5)

# 3️⃣ Remove obvious yield outliers (> 50 tons/hectare)
df_clean = df.filter(col("Avg Yield") < 50)

print("After removing outliers:")
df_clean.describe().show()

# 4️⃣ Fit & save StringIndexer for Crop
crop_indexer = StringIndexer(inputCol="Crop", outputCol="CropIndex")
crop_indexer_model = crop_indexer.fit(df_clean)
crop_indexer_model.write().overwrite().save("crop_indexer")

df_indexed = crop_indexer_model.transform(df_clean)

# 5️⃣ Fit & save StringIndexer for State
state_indexer = StringIndexer(inputCol="State", outputCol="StateIndex")
state_indexer_model = state_indexer.fit(df_indexed)
state_indexer_model.write().overwrite().save("state_indexer")

df_indexed = state_indexer_model.transform(df_indexed)

# 6️⃣ Fit & save OneHotEncoder for CropIndex and StateIndex
encoder = OneHotEncoder(
    inputCols=["CropIndex", "StateIndex"],
    outputCols=["CropVec", "StateVec"]
)
encoder_model = encoder.fit(df_indexed)
encoder_model.write().overwrite().save("crop_state_encoder")

df_encoded = encoder_model.transform(df_indexed)

# 7️⃣ Define numeric features
numeric_features = [
    "Avg Area",
    "Avg Agri Land",
    "Avg Barren Land",
    "Avg Rainfall",
    "Fertilizer per ha",
    "Pesticide per ha"
]

# 8️⃣ Assemble numeric + CropVec + StateVec into single feature vector
assembler = VectorAssembler(
    inputCols=numeric_features + ["CropVec", "StateVec"],
    outputCol="features"
)

df_features = assembler.transform(df_encoded)

# 9️⃣ Prepare final data (features + label)
final_data = df_features.select(col("features"), col("Avg Yield").alias("label"))

print("Sample of final training data:")
final_data.show(5)

# 🔟 Split into train/test
train_data, test_data = final_data.randomSplit([0.8, 0.2], seed=42)

# 1️⃣1️⃣ Train Linear Regression model
lr = LinearRegression(featuresCol="features", labelCol="label")
lr_model = lr.fit(train_data)

# 1️⃣2️⃣ Evaluate model
test_results = lr_model.evaluate(test_data)
print(f"RMSE: {test_results.rootMeanSquaredError:.2f}")
print(f"R2: {test_results.r2:.2f}")

# 1️⃣3️⃣ Show predictions
predictions = lr_model.transform(test_data)
predictions.select("features", "label", "prediction").show(5)

# ✅ Save the trained model
lr_model.save("crop_yield_model")

print("✅ Model, crop indexer, state indexer & encoder saved!")

spark.stop()
