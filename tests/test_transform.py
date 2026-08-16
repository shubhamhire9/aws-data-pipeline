# tests/test_transform.py
import pytest
import pandas as pd
import numpy as np

from etl.transform import clean_data, aggregate_data, transform_data

def test_clean_data():
    """Test that clean_data drops rows with nulls."""
    # Create a DataFrame with some nulls
    df = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "value": [100, None, 200, 300],
        "category": ["A", "B", None, "C"]
    })
    
    cleaned = clean_data(df)
    
    # Should drop rows 1 (value null) and 2 (category null)
    assert len(cleaned) == 2
    assert cleaned.iloc[0]["id"] == 1
    assert cleaned.iloc[1]["id"] == 4

def test_aggregate_data():
    """Test that aggregation works correctly."""
    df = pd.DataFrame({
        "category": ["A", "A", "B", "B", "B"],
        "value": [10, 20, 30, 40, 50]
    })
    
    aggregated = aggregate_data(df, group_by="category", agg_col="value", agg_func="mean")
    
    assert len(aggregated) == 2
    assert aggregated.loc[aggregated["category"] == "A", "value_mean"].iloc[0] == 15.0
    assert aggregated.loc[aggregated["category"] == "B", "value_mean"].iloc[0] == 40.0

def test_aggregate_data_missing_column():
    """Test that missing columns raise ValueError."""
    df = pd.DataFrame({"id": [1, 2], "other": [10, 20]})
    
    with pytest.raises(ValueError, match="Column 'category' not found"):
        aggregate_data(df, group_by="category", agg_col="value")

def test_transform_data_full():
    """Test the full transformation pipeline with a realistic dataset."""
    df = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "category": ["A", "B", "A", None, "B"],
        "value": [100, 200, None, 300, 250]
    })
    
    transformed = transform_data(df)
    
    # After cleaning: drop row with None (row 3, index 2)
    # After aggregation: group by category, mean of value
    # Expected: A -> mean(100) = 100, B -> mean(200, 250) = 225
    assert len(transformed) == 2
    assert transformed.loc[transformed["category"] == "A", "value_mean"].iloc[0] == 100.0
    assert transformed.loc[transformed["category"] == "B", "value_mean"].iloc[0] == 225.0