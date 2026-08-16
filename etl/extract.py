# etl/extract.py
import os
import boto3
import pandas as pd
from io import StringIO

def extract_csv_from_s3(bucket: str, key: str, region: str = None) -> pd.DataFrame:
    """
    Read a CSV file from an S3 bucket and return a pandas DataFrame.
    """
    # If region is not provided, use the environment variable or default.
    if region is None:
        region = os.getenv("AWS_REGION", "us-east-1")
    
    # Create an S3 client
    s3_client = boto3.client("s3", region_name=region)
    
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        # Read the CSV content from the response body
        csv_content = response["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(csv_content))
        return df
    except Exception as e:
        raise Exception(f"Failed to read CSV from s3://{bucket}/{key}: {e}")