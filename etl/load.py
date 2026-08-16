# etl/load.py
import os
import boto3
import pandas as pd
from io import BytesIO
import pyarrow.parquet as pq
import pyarrow as pa

def load_parquet_to_s3(df: pd.DataFrame, bucket: str, key: str, region: str = None) -> None:
    """
    Write a pandas DataFrame as Parquet to S3.
    """
    if region is None:
        region = os.getenv("AWS_REGION", "us-east-1")
    
    s3_client = boto3.client("s3", region_name=region)
    
    # Convert DataFrame to Parquet in memory
    table = pa.Table.from_pandas(df)
    buffer = BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)  # Reset buffer position
    
    try:
        s3_client.upload_fileobj(buffer, bucket, key)
        print(f"Successfully wrote Parquet file to s3://{bucket}/{key}")
    except Exception as e:
        raise Exception(f"Failed to upload Parquet to S3: {e}")