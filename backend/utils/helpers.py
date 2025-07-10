from typing import Iterable, List


def normalize(data: Iterable[float]) -> List[float]:
    """Scale numeric values to the range [0.0, 1.0].

    Parameters
    ----------
    data: Iterable[float]
        Sequence of numeric values.

    Returns
    -------
    List[float]
        Normalized values between 0 and 1.
    """
    data_list = list(data)
    if not data_list:
        return []
    min_val = min(data_list)
    max_val = max(data_list)
    if max_val == min_val:
        return [0.0 for _ in data_list]
    return [(x - min_val) / (max_val - min_val) for x in data_list]
