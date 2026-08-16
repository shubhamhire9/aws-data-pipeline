# etl/transform.py
import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning: drop rows with any null values, convert types.
    """
    # Drop rows with any missing values
    df_cleaned = df.dropna()
    # Convert columns to appropriate types if needed
    # Example: if there is a 'date' column, convert to datetime
    # df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], errors='coerce')
    # For numeric columns, ensure they are numeric
    # Here we just return the cleaned df
    return df_cleaned

def aggregate_data(df: pd.DataFrame, group_by: str, agg_col: str, agg_func: str = "mean") -> pd.DataFrame:
    """
    Perform aggregation on the DataFrame.
    """
    if group_by not in df.columns:
        raise ValueError(f"Column '{group_by}' not found in DataFrame")
    if agg_col not in df.columns:
        raise ValueError(f"Column '{agg_col}' not found in DataFrame")
    
    # Use pandas groupby and aggregate
    agg_dict = {agg_col: agg_func}
    aggregated = df.groupby(group_by).agg(agg_dict).reset_index()
    # Rename the aggregated column to include the function name
    aggregated.columns = [group_by, f"{agg_col}_{agg_func}"]
    return aggregated

# We can also combine both steps in a single transformation pipeline
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full transformation: clean, then aggregate.
    We'll set default group_by = 'category' and agg_col = 'value' for demonstration.
    In a real scenario, you'd read these from env or config.
    """
    cleaned = clean_data(df)
    # If there is a 'category' and 'value' column, aggregate
    # Otherwise, we could skip aggregation or fallback to a dummy grouping.
    if 'category' in cleaned.columns and 'value' in cleaned.columns:
        aggregated = aggregate_data(cleaned, group_by='category', agg_col='value', agg_func='mean')
        return aggregated
    else:
        # If the expected columns are missing, just return cleaned data
        return cleaned