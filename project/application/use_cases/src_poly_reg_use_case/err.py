from project.domain.entities.poly_entity import Polynomial
from typing import Tuple, List

def get_error(dataset: List[Tuple[int | float , int | float]], poly: Polynomial) -> float | int:
        err = 0
        for data in dataset:
            err += (data[1] - poly.get_response_at(data[0])) ** 2
        return err