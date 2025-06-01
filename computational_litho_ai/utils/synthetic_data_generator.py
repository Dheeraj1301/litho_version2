import pandas as pd
import numpy as np
import random
import os

def generate_synthetic_litho_data(num_samples=100, save_path="data/raw/synthetic_samples.csv"):
    pattern_ids = range(1, num_samples + 1)
    
    intensities = np.clip(np.random.normal(loc=0.75, scale=0.1, size=num_samples), 0.5, 1.0)
    linewidths = np.random.randint(30, 55, size=num_samples)  # in nanometers
    shapes = random.choices(['L-shape', 'T-shape', 'Line', 'Circle', 'Square'], k=num_samples)
    defect_types = random.choices(['none', 'missing_resist', 'nanoparticle', 'bridge', 'open'], k=num_samples)
    
    df = pd.DataFrame({
        "pattern_id": pattern_ids,
        "intensity": intensities,
        "linewidth_nm": linewidths,
        "shape": shapes,
        "defect_type": defect_types
    })

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"[✔] Synthetic data generated: {save_path}")

if __name__ == "__main__":
    generate_synthetic_litho_data(num_samples=200)
