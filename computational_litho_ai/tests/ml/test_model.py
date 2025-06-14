import torch
import numpy as np
import joblib
from ml.yield_prediction.yield_predictor import YieldPredictor
from ml.gated_cnn.gated_cnn import GatedCNN, predict_layout_class
from ml.autoencoder.autoencoder import AutoEncoder

def test_yield_predictor():
    model = YieldPredictor()
    model.load_model("models/yield_predictor.joblib")

    # Create dummy tabular input (2 features)
    X_test = np.array([[10.0, 5.0]])
    prediction = model.predict(X_test)
    
    assert prediction.shape == (1,)
    print("✅ YieldPredictor test passed. Output:", prediction)


def test_gated_cnn():
    model = GatedCNN()
    model.load_state_dict(torch.load("models/gated_cnn.pt"))
    model.eval()

    # Dummy image input (batch size 1, 1 channel, 64x64)
    dummy_input = torch.randn(1, 1, 64, 64)
    prediction = predict_layout_class(model, dummy_input)

    assert isinstance(prediction, int)
    print("✅ GatedCNN test passed. Predicted class:", prediction)


def test_autoencoder():
    model = AutoEncoder()
    model.load_state_dict(torch.load("models/autoencoder.pt"))
    model.eval()

    # Dummy image input (batch size 1, 1 channel, 64x64)
    dummy_input = torch.randn(1, 1, 64, 64)
    output = model(dummy_input)

    assert output.shape == dummy_input.shape
    print("✅ AutoEncoder test passed. Output shape:", output.shape)


if __name__ == "__main__":
    test_yield_predictor()
    test_gated_cnn()
    test_autoencoder()
