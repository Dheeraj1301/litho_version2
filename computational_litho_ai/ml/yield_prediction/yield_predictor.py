from sklearn.ensemble import GradientBoostingRegressor
import joblib
import os

class YieldPredictor:
    def __init__(self):
        self.model = GradientBoostingRegressor()

    def fit(self, X, y):
        self.model.fit(X, y)
        print("✅ Model training complete.")

    def predict(self, X):
        return self.model.predict(X)

    def save_model(self, path="models/yield_predictor.joblib"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.model, path)
        print(f"✅ Model saved to {path}")

    def load_model(self, path="models/yield_predictor.joblib"):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found at {path}")
        self.model = joblib.load(path)
        print(f"✅ Model loaded from {path}")
