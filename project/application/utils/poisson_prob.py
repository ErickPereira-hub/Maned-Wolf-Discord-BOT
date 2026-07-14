from math import factorial, e, log
from typing import Callable

poisson: Callable[[int | float, int], float] = lambda avg, input_qtt : e ** (log(avg) * input_qtt + ((-1)*avg) - log(factorial(input_qtt))) if avg > 0 else 0

if __name__ == "__main__":
    print(poisson(31.2124, 30) * 100)