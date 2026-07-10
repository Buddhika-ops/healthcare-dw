from pyspark.sql import functions as F
from pyspark.sql import SparkSession

spark = SparkSession.builder \
        .appName("ObservationsTransform") \
        .master("local[*]") \
        .getOrCreate()

df = spark.read.csv("data/raw/raw_observations.csv",
                    header= True,
                    inferSchema= True)

filtered_df = df.filter(F.col("CATEGORY") == "laboratory")
result_df = filtered_df.select(
    F.md5(F.concat_ws("-",F.col("PATIENT"), F.col("ENCOUNTER"), F.col("DATE"))).alias("lab_result_id"),
    F.col("PATIENT").alias("patient_id"),
    F.col("ENCOUNTER").alias("encounter_id"),
    F.col("DATE").alias("result_date"),
    F.col("CODE").alias("code"),
    F.col("DESCRIPTION").alias("description"),
    F.col("VALUE").alias("value"),
    F.col("UNITS").alias("units"),
    F.col("TYPE").alias("value_type"),

)   

result_df.write.csv(
    "data/spark_output/fact_lab_result_spark",
    header= True,
    mode= "overwrite"
)
print(f"Spark job complete. Rows written: {result_df.count()}")
spark.stop()
