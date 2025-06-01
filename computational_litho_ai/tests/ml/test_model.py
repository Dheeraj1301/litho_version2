from backend.ml.model import predict  # Replace with actual function path

def test_predict_output_shape():
    sample_input = {"feature1": 10, "feature2": 5}
    result = predict(sample_input)
    assert isinstance(result, dict)
    assert "prediction" in result
