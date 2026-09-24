from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_trunc, avg

# 🔌 conexão com Spark cluster
spark = SparkSession.builder \
    .appName("bitcoin_transform") \
    .getOrCreate()

# 🔧 config de conexão (centralizada)
POSTGRES_URL = "jdbc:postgresql://192.168.1.23:5432/postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DRIVER = "org.postgresql.Driver"

# 📥 ler do Postgres
df = spark.read \
    .format("jdbc") \
    .option("url", POSTGRES_URL) \
    .option("dbtable", "bitcoin.price") \
    .option("user", POSTGRES_USER) \
    .option("password", POSTGRES_PASSWORD) \
    .option("driver", POSTGRES_DRIVER) \
    .load()

# 🔄 transformação (média por hora)
df_transformed = df \
    .withColumn("dt_hour", date_trunc("hour", col("collected_at"))) \
    .groupBy("dt_hour") \
    .agg(avg("price_brl").alias("avg_price_brl"))

# 📤 salvar de volta
df_transformed.write \
    .format("jdbc") \
    .option("url", POSTGRES_URL) \
    .option("dbtable", "bitcoin.price_hourly") \
    .option("user", POSTGRES_USER) \
    .option("password", POSTGRES_PASSWORD) \
    .option("driver", POSTGRES_DRIVER) \
    .mode("append") \
    .save()

spark.stop()
