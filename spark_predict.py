from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegressionModel
from pyspark.ml.feature import StringIndexerModel, OneHotEncoderModel, VectorAssembler
from pyspark.sql import Row

# 1️⃣ Start Spark session
spark = SparkSession.builder \
    .appName("CropYieldPrediction_Test_WithState") \
    .getOrCreate()

# 2️⃣ Load saved models
lr_model = LinearRegressionModel.load("crop_yield_model")
crop_indexer_model = StringIndexerModel.load("crop_indexer")
state_indexer_model = StringIndexerModel.load("state_indexer")
encoder_model = OneHotEncoderModel.load("crop_state_encoder")

# 3️⃣ Example test input: realistic (State + Crop)
test_rows = [
    Row(
        State="Andhra Pradesh",
        Crop="Arhar/Tur",
        **{
            "Avg Area": 210217.63,
            "Avg Agri Land": 247314.86,
            "Avg Barren Land": 37097.23,
            "Avg Rainfall": 919.42,
            "Fertilizer per ha": 134.46,
            "Pesticide per ha": 0.27
        }
    )
]

# 4️⃣ Create DataFrame
test_df = spark.createDataFrame(test_rows)

# 5️⃣ Apply StringIndexer for Crop & State
df_indexed = crop_indexer_model.transform(test_df)
df_indexed = state_indexer_model.transform(df_indexed)

# 6️⃣ Apply OneHotEncoder for CropIndex & StateIndex
df_encoded = encoder_model.transform(df_indexed)

# 7️⃣ Assemble numeric + CropVec + StateVec into final feature vector
numeric_features = [
    "Avg Area",
    "Avg Agri Land",
    "Avg Barren Land",
    "Avg Rainfall",
    "Fertilizer per ha",
    "Pesticide per ha"
]

assembler = VectorAssembler(
    inputCols=numeric_features + ["CropVec", "StateVec"],
    outputCol="features"
)

final_test_df = assembler.transform(df_encoded)

# 8️⃣ Predict Avg Yield
predictions = lr_model.transform(final_test_df)

# 9️⃣ Show results
result = predictions.select(
    "State", "Crop", *numeric_features, "prediction"
).withColumnRenamed("prediction", "Predicted_Avg_Yield")

result.show(truncate=False)

spark.stop()
