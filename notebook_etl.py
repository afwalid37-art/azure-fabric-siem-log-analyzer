from pyspark.sql.functions import col

# STEP 1: READ (Standard Mode)
# We removed 'multiline' because your file appears to be standard JSON Lines.
df = spark.read.json("Files/server_logs.json")

# STEP 2: TRANSFORM
df_silver = df.select(
    col("TimeCreated"),
    col("EventID"),
    col("Computer"),
    col("EventData.IpAddress").alias("IP_Address"),
    col("EventData.TargetUserName").alias("User_Name"), # This caused the mismatch!
    col("EventData.Status").alias("Logon_Status")
)

# STEP 3: VERIFY
# We must see ~5000 rows. If not, we debug the raw text.
row_count = df_silver.count()
print(f"--- DIAGNOSTICS ---\nTotal Rows Loaded: {row_count}")

if row_count > 100:
    print("Data looks correct. Saving...")
    # STEP 4: WRITE with Schema Overwrite
    # 'overwriteSchema' allows us to change UserName -> User_Name without crashing
    df_silver.write \
        .format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .saveAsTable("silver_security_logs")
    print("SUCCESS: Table schema updated and data saved.")
else:
    print("ERROR: Still finding low row count. Let's inspect the raw file:")
    # This prints the first 3 lines of the file exactly as Spark sees them
    spark.read.text("Files/server_logs.json").show(3, truncate=False)