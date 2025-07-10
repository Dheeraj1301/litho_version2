import numpy as np


def normalize(data):
    arr = np.array(data, dtype=float)
    if arr.size == 0:
        return []
    min_val = arr.min()
    max_val = arr.max()
    if max_val == min_val:
        return [0.0 for _ in arr]
    return list((arr - min_val) / (max_val - min_val))
