import os
import pytest
import boto3
import pandas as pd
from moto import mock_aws
from etl.pipeline import run_pipeline

SAMPLE_CSV = """id,name,category,value
1,Alice,A,100
2,Bob,B,200
3,Charlie,A,150
4,Diana,B,None
5,Eve,C,300
"""

@pytest.fixture
def setup_mock_s3_and_env():
    with mock_aws():
        os.environ["AWS_REGION"] = "us-east-1"
        os.environ["S3_BUCKET"] = "test-bucket"
        os.environ["INPUT_FILE_KEY"] = "input/data.csv"
        os.environ["OUTPUT_FILE_KEY"] = "output/result.parquet"
        
        s3_client = boto3.client("s3", region_name="us-east-1")
        s3_client.create_bucket(Bucket="test-bucket")
        s3_client.put_object(Bucket="test-bucket", Key="input/data.csv", Body=SAMPLE_CSV.encode("utf-8"))
        yield

def test_full_pipeline_integration(setup_mock_s3_and_env):
    run_pipeline()
    
    s3_client = boto3.client("s3", region_name="us-east-1")
    response = s3_client.get_object(Bucket="test-bucket", Key="output/result.parquet")
    import pyarrow.parquet as pq
    from io import BytesIO
    body = response["Body"].read()
    table = pq.read_table(BytesIO(body))
    df = table.to_pandas()
    
    expected = pd.DataFrame({"category": ["A", "B", "C"], "value_mean": [125.0, 200.0, 300.0]})
    df = df.sort_values("category").reset_index(drop=True)
    expected = expected.sort_values("category").reset_index(drop=True)
    pd.testing.assert_frame_equal(df, expected)