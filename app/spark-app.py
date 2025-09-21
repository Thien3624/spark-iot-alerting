from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, window, current_timestamp, when
from pyspark.sql.types import StructType, DoubleType
import logging

spark = SparkSession.builder.appName("IoTTempAlert").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

logging.getLogger("py4j").setLevel(logging.ERROR)
logging.getLogger("org.apache.spark").setLevel(logging.ERROR)
logging.getLogger("org.spark_project").setLevel(logging.ERROR)

schema = StructType().add("temperature", DoubleType())

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "iot_temperature") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

avg_temp = json_df.withColumn("ts", current_timestamp()) \
    .groupBy(window(col("ts"), "10 seconds")) \
    .agg(avg("temperature").alias("avg_temp"))

result = avg_temp.withColumn("alert", when(col("avg_temp") > 40, "ALERT").otherwise("OK"))

query = result.writeStream.outputMode("update").format("console").start()
query.awaitTermination()
