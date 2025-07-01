from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegressionModel
from pyspark.ml.feature import StringIndexerModel, OneHotEncoderModel, VectorAssembler
from pyspark.sql import Row

# 1️⃣ Start Spark session
spark = SparkSession.builder.appName("CropYieldPrediction_Test_WithState").getOrCreate()

# 2️⃣ Load saved model & transformers
lr_model = LinearRegressionModel.load("crop_yield_model")
crop_indexer_model = StringIndexerModel.load("crop_indexer")
state_indexer_model = StringIndexerModel.load("state_indexer")
encoder_model = OneHotEncoderModel.load("crop_state_encoder")

# 3️⃣ 5 realistic test cases (State + Crop + features)
test_rows = [
    Row(
        State="Punjab",
        Crop="Wheat",
        **{
            "Avg Area": 400000.0,
            "Avg Agri Land": 450000.0,
            "Avg Barren Land": 50000.0,
            "Avg Rainfall": 700.0,
            "Fertilizer per ha": 220.0,
            "Pesticide per ha": 0.4
        }
    ),
    Row(
        State="Uttar Pradesh",
        Crop="Rice",
        **{
            "Avg Area": 600000.0,
            "Avg Agri Land": 700000.0,
            "Avg Barren Land": 80000.0,
            "Avg Rainfall": 1400.0,
            "Fertilizer per ha": 180.0,
            "Pesticide per ha": 0.5
        }
    ),
    Row(
        State="Maharashtra",
        Crop="Sugarcane",
        **{
            "Avg Area": 250000.0,
            "Avg Agri Land": 270000.0,
            "Avg Barren Land": 20000.0,
            "Avg Rainfall": 1100.0,
            "Fertilizer per ha": 240.0,
            "Pesticide per ha": 0.35
        }
    ),
    Row(
        State="Andhra Pradesh",
        Crop="Arhar/Tur",
        **{
            "Avg Area": 200000.0,
            "Avg Agri Land": 240000.0,
            "Avg Barren Land": 40000.0,
            "Avg Rainfall": 900.0,
            "Fertilizer per ha": 130.0,
            "Pesticide per ha": 0.3
        }
    ),
    Row(
        State="Karnataka",
        Crop="Maize",
        **{
            "Avg Area": 150000.0,
            "Avg Agri Land": 180000.0,
            "Avg Barren Land": 30000.0,
            "Avg Rainfall": 850.0,
            "Fertilizer per ha": 160.0,
            "Pesticide per ha": 0.25
        }
    )
]

# 4️⃣ Create DataFrame
test_df = spark.createDataFrame(test_rows)

# 5️⃣ Apply Crop + State indexers
df_indexed = crop_indexer_model.transform(test_df)
df_indexed = state_indexer_model.transform(df_indexed)

# 6️⃣ Apply combined OneHotEncoder
df_encoded = encoder_model.transform(df_indexed)

# 7️⃣ Assemble final feature vector
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

# 9️⃣ Show result
result = predictions.select(
    "State", "Crop", *numeric_features, "prediction"
).withColumnRenamed("prediction", "Predicted_Avg_Yield")

result.show(truncate=False)

spark.stop()
