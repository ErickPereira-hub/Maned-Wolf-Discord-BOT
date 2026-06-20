class SingleProbNewMembersView:

    def __init__(self, prob: float, from_qtt: int, to_qtt: int):
        self.__prob: float = prob
        self.__from_qtt: int = from_qtt
        self.__to_qtt: int = to_qtt
    
    def __str__(self) -> str:
        self.__tprob: float = self.__prob * 100
        self.__MSG: str = f" ⚡ Probability of gaining {self.__from_qtt} to {self.__to_qtt} new members tomorrow: {self.__tprob:.3f}%"
        if self.__tprob < 10:
            self.__MSG += " (Unlikely)"
        elif self.__tprob < 50:
            self.__MSG += " (Possible)"
        else:
            self.__MSG += " (Trustable)"
        return self.__MSG