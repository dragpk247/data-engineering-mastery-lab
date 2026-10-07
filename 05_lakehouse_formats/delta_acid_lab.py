"""
05_lakehouse_formats/delta_acid_lab.py
--------------------------------------
Demonstrates Delta Lake Open Table Format.
Key concepts:
- ACID Transactions on Parquet
- Transaction Log (_delta_log)
- Time-Travel (querying previous snapshots)
- Schema enforcement
"""

import os
import shutil
from pyspark.sql import SparkSession

DATA_PATH = "/tmp/delta_acid_lab_table"

def main():
    print("=" * 65)
    print("🔺 Delta Lake Open Table Format Lab (ACID & Time Travel)")
    print("=" * 65)

    if os.path.exists(DATA_PATH):
        shutil.rmtree(DATA_PATH)

    spark = SparkSession.builder \
        .appName("DeltaAcidLab") \
        .master("local[*]") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # 1. Version 0: Initial Commit
    print("\n--- 1. Commit Version 0: Initial Users ---")
    v0_data = [("U1", "active", 100), ("U2", "pending", 50)]
    df_v0 = spark.createDataFrame(v0_data, ["user_id", "status", "points"])
    df_v0.write.format("delta").mode("overwrite").save(DATA_PATH)
    
    print("Snapshot at Version 0:")
    spark.read.format("delta").load(DATA_PATH).show()

    # 2. Version 1: Updating and Appending records (ACID commit)
    print("\n--- 2. Commit Version 1: Append New Users ---")
    v1_data = [("U3", "active", 300), ("U4", "active", 150)]
    df_v1 = spark.createDataFrame(v1_data, ["user_id", "status", "points"])
    df_v1.write.format("delta").mode("append").save(DATA_PATH)

    print("Current State (Version 1):")
    spark.read.format("delta").load(DATA_PATH).show()

    # 3. TIME TRAVEL: Reading historical snapshot
    print("\n--- 3. Time Travel Query: Reading Version 0 as it existed historically ---")
    df_historical = spark.read.format("delta").option("versionAsOf", 0).load(DATA_PATH)
    df_historical.show()

    print("=" * 65)
    print("✅ Delta Lake Lab Finished Successfully!")
    print("=" * 65)

    spark.stop()

if __name__ == "__main__":
    main()
