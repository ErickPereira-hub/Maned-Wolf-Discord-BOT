from project.domain.entities.poly_entity import Polynomial
from typing import Tuple, List

def get_error(dataset: List[Tuple[int | float , int | float]],
            poly: Polynomial,
            training_data: bool = False) -> float | int:
        err: int | None = None
        #If we are not training the data, the return is in %
        if not training_data:
            sum_: int | float = 0
            for data in dataset:
                sum_ += abs((data[1] - poly.get_response_at(data[0])) / data[1])
            err = 100 * (sum_ / len(dataset))
            return err
        
        #If we are training the data, the return is the Minimum Squared Value
        err = sum((data[1] - poly.get_response_at(data[0])) ** 2 for data in dataset)
        return err