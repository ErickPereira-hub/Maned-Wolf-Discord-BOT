from typing import Dict, Tuple, List
from project.application.utils.std_deviation import get_std_deviation

def add_acum_freq_middleware(resp_input: Dict[str, str | Tuple[int, int, int]]) -> Dict[str, Tuple[int, int, int]]:
    resp_middle: Dict[str, Tuple[int, int, int, int]] = dict()
    new: int = 0
    for k, v in resp_input["data"].items():
        new += v[2]
        resp_middle.update({k : (v[0], v[1], v[2], new)})
    
    resp: Dict[str, str | Tuple[int, int, int, int]] = {"data": resp_middle}

    resp.update({
        "overall_tot_avg" : sum([value[3] for value in resp_middle.copy().values()]) / len(resp_middle.copy()),
        "overall_tot_std_dev" : get_std_deviation([value[3] for value in resp_middle.copy().values()]),
        "overall_var_avg" : sum([value[2] for value in resp_middle.copy().values()]) / len(resp_middle.copy()),
        "overall_var_std_dev" : get_std_deviation([value[2] for value in resp_middle.copy().values()]), 
        "message": resp_input["message"]
            })
    
    return resp