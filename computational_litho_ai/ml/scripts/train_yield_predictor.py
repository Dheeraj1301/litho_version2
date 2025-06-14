import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import numpy as np
from ml.yield_prediction.yield_predictor import YieldPredictor

# Dummy data
X = np.random.rand(100, 5)
y = np.random.rand(100)

model = YieldPredictor()
model.fit(X, y)
model.save_model("models/yield_predictor.joblib")
