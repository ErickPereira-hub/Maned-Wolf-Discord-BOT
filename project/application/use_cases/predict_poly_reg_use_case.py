from typing import List, Tuple, Any, Dict
from project.application.use_cases.src_poly_reg_use_case import get_best_deg_info
from project.domain.entities.poly_entity import Polynomial

def predict_poly_reg_use_case(input: float | int, dataset: List[Tuple[int | float , int | float]], from_deg: int = 1, until_deg: int = 5) -> Dict[str, float | int]:
    info_of_the_best: Dict[str, Any] =  get_best_deg_info(dataset, from_deg, until_deg)
    poly: Polynomial = info_of_the_best["polynomial"]
    err: int | float = info_of_the_best["ERROR"]
    predicted_output: float | int = poly.get_response_at(input)
    return {"predicted_output": predicted_output, "error" : err, "polynomial": str(poly)}