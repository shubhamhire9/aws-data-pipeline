# etl/pipeline.py
import os
import sys
from dotenv import load_dotenv
from etl.extract import extract_csv_from_s3
from etl.transform import transform_data
from etl.load import load_parquet_to_s3

def run_pipeline():
    """
    Main ETL pipeline.
    """
    # Load environment variables from .env file if present
    load_dotenv()
    
    # Read configuration
    bucket = os.getenv("S3_BUCKET")
    input_key = os.getenv("INPUT_FILE_KEY")
    output_key = os.getenv("OUTPUT_FILE_KEY")
    region = os.getenv("AWS_REGION", "us-east-1")
    
    if not bucket or not input_key or not output_key:
        print("ERROR: Missing required environment variables.")
        print("Please set S3_BUCKET, INPUT_FILE_KEY, OUTPUT_FILE_KEY")
        sys.exit(1)
    
    print(f"Starting ETL pipeline for bucket: {bucket}, input: {input_key}, output: {output_key}")
    
    # Extract
    print("Extracting data...")
    df = extract_csv_from_s3(bucket, input_key, region)
    print(f"Extracted {len(df)} rows.")
    
    # Transform
    print("Transforming data...")
    transformed_df = transform_data(df)
    print(f"Transformed to {len(transformed_df)} rows.")
    
    # Load
    print("Loading data...")
    load_parquet_to_s3(transformed_df, bucket, output_key, region)
    
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()