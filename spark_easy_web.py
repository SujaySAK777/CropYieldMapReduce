# ✅ FILE: spark_easy_web.py

import sys
from pyspark.sql import SparkSession, Row
from pyspark.ml.regression import LinearRegressionModel
from pyspark.ml.feature import StringIndexerModel, OneHotEncoderModel, VectorAssembler

# Take arguments from command line
state = sys.argv[1]
crop = sys.argv[2]
avg_area = float(sys.argv[3])
avg_agri_land = float(sys.argv[4])
avg_barren_land = float(sys.argv[5])
avg_rainfall = float(sys.argv[6])
fertilizer_per_ha = float(sys.argv[7])
pesticide_per_ha = float(sys.argv[8])

spark = SparkSession.builder.appName("CropYieldPrediction_Test_WithState").getOrCreate()

# Load saved models
lr_model = LinearRegressionModel.load("crop_yield_model")
crop_indexer_model = StringIndexerModel.load("crop_indexer")
state_indexer_model = StringIndexerModel.load("state_indexer")
encoder_model = OneHotEncoderModel.load("crop_state_encoder")

test_row = Row(
    State=state,
    Crop=crop,
    **{
        "Avg Area": avg_area,
        "Avg Agri Land": avg_agri_land,
        "Avg Barren Land": avg_barren_land,
        "Avg Rainfall": avg_rainfall,
        "Fertilizer per ha": fertilizer_per_ha,
        "Pesticide per ha": pesticide_per_ha
    }
)

test_df = spark.createDataFrame([test_row])
df_indexed = crop_indexer_model.transform(test_df)
df_indexed = state_indexer_model.transform(df_indexed)
df_encoded = encoder_model.transform(df_indexed)

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
predictions = lr_model.transform(final_test_df)

result = predictions.select(
    "State", "Crop", *numeric_features, "prediction"
).withColumnRenamed("prediction", "Predicted_Avg_Yield")

# Save to CSV
result.toPandas().to_csv("prediction_result.csv", index=False)

spark.stop()
