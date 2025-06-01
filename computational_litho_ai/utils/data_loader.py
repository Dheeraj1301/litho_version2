import pandas as pd
import os

def load_data(file_path: str = "data/sample_data.csv") -> pd.DataFrame:
    """
    Load the synthetic lithography data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset as a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at: {file_path}")

    try:
        df = pd.read_csv(file_path)
        print(f"[INFO] Data loaded successfully from {file_path}")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        raise


def preview_data(df: pd.DataFrame, num_rows: int = 5):
    """
    Display the first few rows of the dataset.

    Args:
        df (pd.DataFrame): The DataFrame to preview.
        num_rows (int): Number of rows to preview.
    """
    print(f"[INFO] Previewing the first {num_rows} rows of the dataset:")
    print(df.head(num_rows))


def summarize_data(df: pd.DataFrame):
    """
    Show summary statistics and info for the dataset.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    print("\n[INFO] Data Summary:")
    print(df.describe())

    print("\n[INFO] Data Types:")
    print(df.dtypes)

    print("\n[INFO] Missing Values:")
    print(df.isnull().sum())
