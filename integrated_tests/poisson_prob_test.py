from project.application.poisson_member import PoissonMember
from typing import List

def test_poisson() -> None:

    #Mocked data
    #number of new members for the last 11 days
    mocked_dataset: List[int | float] = [1, 2, 2, 3, 1, 2, 3, 4, 5, 4, 3]
    mocked_from: int | float = [1, 2, 4]
    mocked_until: int | float = [5, 10, 4]

    probability: List[float] = list() #<--- Least of Poisson's probabilities

    for vmocked_from, vmocked_until in zip(mocked_from, mocked_until):
        probability.append(PoissonMember().get_poisson_in_range(
            from_qtt = vmocked_from,
            until_qtt = vmocked_until,
            incrs = mocked_dataset
        )) #<--- Must return the probability of having from 1 to 5, 2 to 5 and 4 new members for the last 7 days considering the dataset, where each data is the number of entrances for each day, with each position as a day. The bigger the index, more close we are to today

    real_probability = [0.85784, 0.82077, 0.17545] #<--- Result taken from a Poisson calculator in internet
    LIM_ERROR: float = 0.01 #<--- Error must be lower than this value
    
    #Checking if the distance is lower than the error
    for vprobability, vreal_probability in zip(probability, real_probability):
        assert abs(vprobability - vreal_probability) < LIM_ERROR