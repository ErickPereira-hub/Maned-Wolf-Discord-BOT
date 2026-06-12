from typing import Any, List

def list_int(val: Any):
    if not isinstance(val, list):
        raise Exception("The input must be a list")
    return [int(el) for el in val]

def list_str(val: Any):
    if not isinstance(val, list):
        raise Exception("The input must be a list")
    return [str(el) for el in val]