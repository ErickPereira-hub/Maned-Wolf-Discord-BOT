from math import factorial, e, log
from typing import Callable

poisson: Callable[[int | float, int], float] = lambda avg, input_qtt : e ** (log(avg) * input_qtt + (-avg) - log(factorial(input_qtt)))

if __name__ == "__main__":
    print(poisson(3, 3) * 100)