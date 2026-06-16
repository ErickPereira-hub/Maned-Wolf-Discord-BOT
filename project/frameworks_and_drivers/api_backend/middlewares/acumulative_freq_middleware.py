from typing import Dict, Tuple, List

def add_acum_freq_middleware(freq_dataset: Dict[str, Tuple[int, int, int]]) -> Dict[str, Tuple[int, int, int]]:
    resp: Dict[str, Tuple[int, int, int, int]] = dict()
    new: int = 0
    for k, v in freq_dataset.items():
        new += v[2]
        resp.update({k : (v[0], v[1], v[2], new)})
    return resp

if __name__ == "__main__":
    print(add_acum_freq_middleware({"A": (1, 2, 3), "B": (2, 1, 1), "C": (3, 2, -1), "D": (1, 1, 1)}))