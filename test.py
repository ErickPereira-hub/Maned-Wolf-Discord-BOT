from project.application.use_cases.predict_poly_reg_use_case import predict_poly_reg_use_case
from pprint import pprint

pprint(predict_poly_reg_use_case(12, [(1, 1.11), (2, 3.114), (3, 9), (4, 16), (5, 25), (6, 36), (7, 49), (8, 64), (9, 81), (10, 100)], 1, 7), width = 120)