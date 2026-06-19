from project.domain.entities.poly_entity import Polynomial
from typing import Tuple, List

def get_error(dataset: List[Tuple[int | float , int | float]], poly: Polynomial) -> float | int:
        sum_ = 0
        for data in dataset:
            sum_ += abs((data[1] - poly.get_response_at(data[0])) / data[1])
        err = 100 * (sum_ / len(dataset))
        return err