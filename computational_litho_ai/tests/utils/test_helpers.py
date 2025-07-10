from utils.helpers import normalize

def test_normalize():
    data = [10, 20, 30]
    output = normalize(data)
    assert isinstance(output, list)
    assert max(output) <= 1.0
    assert min(output) >= 0.0
