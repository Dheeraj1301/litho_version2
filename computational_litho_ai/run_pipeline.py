import os
import pandas as pd
from utils.data_loader import load_data, preview_data, summarize_data
from ml.yield_prediction.yield_predictor import YieldPredictor

def preprocess_data(df):
    # Simple example preprocessing
    df_processed = pd.get_dummies(df)
    return df_processed

def main():
    data_path = "data/raw/synthetic_samples.csv"

    # Step 1: Load data
    try:
        df = load_data(data_path)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return

    # Step 2: Preview and summarize
    preview_data(df)
    summarize_data(df)

    # Step 3: Preprocess data
    df_processed = preprocess_data(df)

    # Assume last column is target
    X = df_processed.iloc[:, :-1]
    y = df_processed.iloc[:, -1]

    # Initialize model
    model = YieldPredictor()

    model_path = "models/yield_predictor.joblib"

    # Check if saved model exists, else train and save
    if os.path.exists(model_path):
        model.load_model(model_path)
    else:
        model.fit(X, y)
        model.save_model(model_path)

    # Step 4: Predict (using the same data here for demo)
    predictions = model.predict(X)
    print("\n✅ Inference complete. Sample predictions:")
    print(predictions[:5])

if __name__ == "__main__":
    main()
