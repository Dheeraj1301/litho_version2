# test_data_loader.py
import os
print("Current Working Directory:", os.getcwd())
print("Files in data/:", os.listdir("data"))

from utils.data_loader import load_data, preview_data, summarize_data

df = load_data("data/raw/synthetic_samples.csv")
preview_data(df)
summarize_data(df)
