from project.domain.entities.poly_entity import Polynomial
from project.application.use_cases.src_poly_reg_use_case.reg import RegressionFactory
from typing import List, Tuple, Dict, Any
from project.application.use_cases.src_poly_reg_use_case.err import get_error

def get_best_deg_info(dataset: List[Tuple[int | float , int | float]], from_deg: int, until_deg: int) -> Dict[str, Any]:
    relation: Dict[Polynomial, float | int] = dict()
    for deg in range(from_deg, until_deg + 1):
        rf: RegressionFactory = RegressionFactory(dataset, deg)
        poly: Polynomial = rf.get_best_poly()
        ERROR: int | float = get_error(dataset, poly)
        relation.update({poly : ERROR})
    MIN_ERR = min(err for err in relation.values())
    for poly, ERR in relation.items():
        if ERR == MIN_ERR:
            resp: Dict[str, Any] = {
                "polynomial": poly,
                "ERROR": ERR
            }
            return resp

if __name__ == "__main__":
    print(get_best_deg_info([(1, 1), (2, 3.98), (3, 9.11), (4, 16), (5, 25), (6, 36.01), (7, 48.98), (8, 64.98), (9, 82)], 1, 5))