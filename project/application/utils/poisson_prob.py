from math import factorial, e
from typing import Callable

poisson: Callable[[int | float, int], float] = lambda avg, input_qtt : ((avg ** input_qtt) * (e ** (-avg))) / factorial(input_qtt)

if __name__ == "__main__":
    print(poisson(10, 10))