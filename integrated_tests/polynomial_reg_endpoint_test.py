from typing import Tuple, List, Dict, Callable
from project.application.use_cases.predict_poly_reg_use_case import predict_poly_reg_use_case

def scrap_poly(poly: str) -> List[float]:
    scrapping_coeffs: List[float] = poly.split(" ")
    scrapping_coeffs = [data for data in scrapping_coeffs if data != "p(x)" and data != "="]
    new_format = [scrapping_coeffs[0]]
    for i in range(1, len(scrapping_coeffs) - 1):
        if scrapping_coeffs[i] == "-":
            new_format.append("-" + scrapping_coeffs[i + 1])
        if scrapping_coeffs[i] == "+":
            new_format.append(scrapping_coeffs[i + 1])
    scrapping_coeffs = new_format
    scrapping_coeffs = [data if ind == 0 else data[0:-3] for ind, data in enumerate(scrapping_coeffs)]
    scrapping_coeffs = [float(data) for data in scrapping_coeffs] #<--- Extracted coefficients from the backend (deg 0 to deg 5 ->)
    return scrapping_coeffs

def test_poly_reg_endpoint(mocker) -> None:

    mocked_dataset: List[Tuple[int, float]] = [
        (1, 256),
        (2, 258),
        (3, 259),
        (4, 261),
        (5, 269),
        (6, 275),
        (7, 272),
        (8, 270),
        (9, 278),
        (10, 289)
    ]

    #The best polynomial from degree 1 to 5 for this situation is the following polynomial
    #best_fit: Callable[[int, float], float] = lambda x : 0.011 * x ** 5 - 0.2426 * x ** 4 + 1.7769 * x ** 3 - 4.7299 * x ** 2 + 5.5123 * x + 254.0667


    JSON: Dict[str, float | int] = predict_poly_reg_use_case(
        input = 0, #<--- We aren't testing the input, just the polynomial precision
        dataset = mocked_dataset
    )

    extracted_coeffs: List[float] = scrap_poly(JSON["polynomial"])
    correct_coeffs = [254.0667, 5.5123, -4.7299, 1.7769, -0.2426, 0.011] #Correct coefficients (deg 0 to deg 5 ->)

    ERROR_COEF: float = 0.001

    assert JSON["error"] >= 0 #<--- FAILED if the error is negative, PASSED otherwise
    
    for coeffs in list(zip(extracted_coeffs, correct_coeffs)):
        assert abs(coeffs[0] - coeffs[1]) < ERROR_COEF