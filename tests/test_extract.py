import pytest
import boto3
import pandas as pd
from io import StringIO
from moto import mock_aws

from etl.extract import extract_csv_from_s3

SAMPLE_CSV = """id,name,category,value
1,Alice,A,100
2,Bob,B,200
3,Charlie,A,150
"""

@pytest.fixture
def s3_bucket_and_key():
    bucket = "test-bucket"
    key = "input/data.csv"
    
    with mock_aws():
        s3_client = boto3.client("s3", region_name="us-east-1")
        s3_client.create_bucket(Bucket=bucket)
        s3_client.put_object(Bucket=bucket, Key=key, Body=SAMPLE_CSV.encode("utf-8"))
        yield bucket, key

def test_extract_csv_from_s3(s3_bucket_and_key):
    bucket, key = s3_bucket_and_key
    df = extract_csv_from_s3(bucket, key)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    # ... rest of assertions

def test_extract_csv_from_s3_invalid_key():
    with mock_aws():
        s3_client = boto3.client("s3", region_name="us-east-1")
        s3_client.create_bucket(Bucket="test-bucket")
        with pytest.raises(Exception, match="Failed to read CSV"):
            extract_csv_from_s3("test-bucket", "missing.csv")