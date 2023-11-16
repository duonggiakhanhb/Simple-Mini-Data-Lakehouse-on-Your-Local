import pyspark
from pyspark.sql import SparkSession
import os


## DEFINE SENSITIVE VARIABLES
NESSIE_URI = os.environ.get("NESSIE_URI") ## Nessie Server URI
DATALAKEHOUSE = os.environ.get("DATALAKEHOUSE") ## BUCKET TO WRITE DATA TOO
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY") ## AWS CREDENTIALS
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY") ## AWS CREDENTIALS
AWS_S3_ENDPOINT= os.environ.get("AWS_S3_ENDPOINT") ## MINIO ENDPOINT


print(AWS_S3_ENDPOINT)
print(NESSIE_URI)
print(DATALAKEHOUSE)


conf = (
    pyspark.SparkConf()
        .setAppName('SQLiteToIceberg')
        .set('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.3.1' +\
        ',org.projectnessie.nessie-integrations:nessie-spark-extensions-3.3_2.12:0.67.0' +\
        ',org.xerial:sqlite-jdbc:3.43.2.2' +\
        ',software.amazon.awssdk:bundle:2.17.178,software.amazon.awssdk:url-connection-client:2.17.178')
        .set('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions,org.projectnessie.spark.extensions.NessieSparkSessionExtensions')
        .set('spark.sql.catalog.nessie', 'org.apache.iceberg.spark.SparkCatalog')
        .set('spark.sql.catalog.nessie.uri', NESSIE_URI)
        .set('spark.sql.catalog.nessie.ref', 'main')
        .set('spark.sql.catalog.demo.s3.path-style-access', 'true')
        .set('spark.sql.catalog.nessie.authentication.type', 'NONE')
        .set('spark.sql.catalog.nessie.catalog-impl', 'org.apache.iceberg.nessie.NessieCatalog')
        .set('spark.sql.catalog.nessie.s3.endpoint', AWS_S3_ENDPOINT)
        .set('spark.sql.catalog.nessie.warehouse', DATALAKEHOUSE)
        .set('spark.sql.catalog.nessie.io-impl', 'org.apache.iceberg.aws.s3.S3FileIO')
        .set('spark.hadoop.fs.s3a.access.key', AWS_ACCESS_KEY)
        .set('spark.hadoop.fs.s3a.secret.key', AWS_SECRET_KEY)
)


## Start Spark Session
spark = SparkSession.builder.config(conf=conf).getOrCreate()
print("Spark Running")
print(f'The PySpark {spark.version} version is running...')
spark.sql("USE nessie")
# Define a list of tables
tables = ["customers", "accounts", "creditCards", "investments", "transactions"]

# Loop through the tables
for table in tables:
    # Load data from SQLite into a Spark DataFrame
    sqlite_df = spark.read.format("jdbc") \
        .option("url", "jdbc:sqlite:db/bank_data.db") \
        .option("dbtable", f"(SELECT * FROM {table}) AS tmp") \
        .option("driver", "org.sqlite.JDBC") \
        .load()
    
    sqlite_df.printSchema()
    # Define the Iceberg table name
    iceberg_table_name = f"nessie.{table}"
    ## Create a Table
    spark.sql(f"CREATE TABLE IF NOT EXISTS {iceberg_table_name} (name STRING) USING iceberg;").show()

    # Check if the table exists

    sqlite_df.write.format('iceberg').mode('overwrite').saveAsTable(iceberg_table_name)

# Stop the Spark session
spark.stop()
print("Success!")
