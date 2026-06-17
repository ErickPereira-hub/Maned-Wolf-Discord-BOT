from math import sqrt
from typing import List

def get_std_deviation(dataset: List[int | float], avg: float | None = None) -> float:
    average: int | None = avg
    if average is None:
        average = sum(data for data in dataset) / len(dataset)
    std_deviation: float = sqrt(sum((x - average) ** 2 for x in dataset) / len(dataset))
    return std_deviation