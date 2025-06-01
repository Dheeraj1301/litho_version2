from utils.synthetic_data_generator import generate_synthetic_litho_data
import os

def test_data_generation():
    path = "data/raw/test_sample.csv"
    generate_synthetic_litho_data(50, save_path=path)
    assert os.path.exists(path)
    print("[✔] Test Passed: Synthetic data file created.")
