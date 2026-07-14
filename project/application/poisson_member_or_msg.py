from project.application.utils.poisson_prob import poisson
from typing import List, Tuple

class PoissonMemberOrMessage:

    def __init__(self):
        self.__avg: float | int | None = None
        self.__last_days_data: List[float | int] | None = None

    def __get_avg_for_last_days(self, incrs: List[float | int], last_days_num: int = 7) -> float | int:
        #The incrs must be a list with the increments for each data since the beginning of the tracking
        #The increments must be in ascending mode from the first day until today
        self.__last_days_data = incrs[(-1) * last_days_num:] #<--- Getting the last days data
        self.__mavg: float | int = sum(self.__last_days_data) / len(self.__last_days_data)
        return self.__mavg
    
    def get_poisson_single_prob(self, input_qtt: int, incrs: List[float | int], last_days: int = 7) -> float:
        self.__avg = self.__get_avg_for_last_days(incrs = incrs, last_days_num = last_days)
        return poisson(self.__avg, input_qtt)

    def get_poisson_in_range(self, from_qtt: int, until_qtt: int, incrs: List[int | float], last_days: int = 7) -> float:
        self.__avg = self.__get_avg_for_last_days(incrs = incrs, last_days_num = last_days)
        #Checking if the range of quantities is following the constraints
        if from_qtt > until_qtt or from_qtt < 0:
            raise ValueError("from_qtt and until_qtt aren't following their constraints")
        if not isinstance(from_qtt, int) or not isinstance(until_qtt, int):
            raise TypeError("Wrong type for from_qtt or until_qtt")
        
        probability: float = sum(poisson(self.__avg, qtt) for qtt in range(from_qtt, until_qtt + 1))
        return probability

    def get_discrete_points(self, incrs: List[int | float], until: int, dist_size: int) -> List[Tuple[int, float]]:
        self.__dist_limit: int = dist_size if dist_size > until else until + 5
        self.__region: range = range(0, self.__dist_limit + 1)
        self.__dist_discrete_points: List[Tuple[int, float]] = list(zip(
            [pos for pos in self.__region],
            [
                self.get_poisson_single_prob(input_qtt = pos, incrs = incrs) for pos in self.__region
            ]))
        return self.__dist_discrete_points