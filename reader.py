from databricksx12 import EDI, HealthcareManager
from pyspark.sql import SparkSession
import json
import pandas as pd

# Initialize Spark Session
spark = SparkSession.builder.appName("SingleEDIProcessing").getOrCreate()

# File path for the single EDI file
edi_file_path = "generated_837_files/fake_837_1.txt"

# Initialize the HealthcareManager for parsing EDI transactions
hm = HealthcareManager()

# Read the single EDI file as text (using wholetext to get the full content in one row)
df = spark.read.text(edi_file_path, wholetext=True)

# Parse the EDI file contents, extract key fields, and convert them to JSON format
rdd = (
    df.rdd
    .map(lambda x: EDI(x.value))  # Parse EDI content
    .map(lambda edi_obj: hm.to_json(edi_obj))  # Convert to JSON using HealthcareManager
)

# Convert RDD of JSON records to a Spark DataFrame
claims_df = spark.read.json(rdd.map(lambda x: json.dumps(x)))

# Show parsed data structure for verification
claims_df.show(truncate=False)

# Convert the Spark DataFrame to Pandas for CSV export
claims_pd = claims_df.toPandas()

# Save as a flat CSV file
output_csv_path = "parsed_single_837_claims.csv"
claims_pd.to_csv(output_csv_path, index=False)

print(f"Parsed data saved to {output_csv_path}")
