import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import joblib

class YieldPredictor:
    def __init__(self):
        self.model = GradientBoostingRegressor()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def save_model(self, path="ml/yield_prediction/yield_model.pkl"):
        joblib.dump(self.model, path)

    def load_model(self, path="ml/yield_prediction/yield_model.pkl"):
        self.model = joblib.load(path)
