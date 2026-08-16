import pytest
import boto3
import pandas as pd
from io import BytesIO
from moto import mock_aws
import pyarrow.parquet as pq

from etl.load import load_parquet_to_s3

@pytest.fixture
def mock_s3_bucket():
    with mock_aws():
        s3_client = boto3.client("s3", region_name="us-east-1")
        s3_client.create_bucket(Bucket="test-bucket")
        yield "test-bucket"

def test_load_parquet_to_s3(mock_s3_bucket):
    bucket = mock_s3_bucket
    key = "output/processed.parquet"
    df = pd.DataFrame({"category": ["A", "B"], "value_mean": [100.0, 225.0]})
    
    load_parquet_to_s3(df, bucket, key)
    
    s3_client = boto3.client("s3", region_name="us-east-1")
    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = response["Body"].read()
    table = pq.read_table(BytesIO(body))
    loaded_df = table.to_pandas()
    pd.testing.assert_frame_equal(df, loaded_df)

def test_load_parquet_to_s3_invalid_bucket():
    df = pd.DataFrame({"col": [1, 2]})
    with mock_aws():
        # no bucket created – should fail
        with pytest.raises(Exception, match="Failed to upload Parquet"):
            load_parquet_to_s3(df, "non-existent-bucket", "test.parquet")