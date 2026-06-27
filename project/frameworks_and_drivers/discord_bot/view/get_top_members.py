from typing import List, Dict
from project.application.utils.max_str_size import get_max_str_size

class GetTopMembersView:

    def __init__(self, data: List[Dict[str, int]], hours: int, option: str):
        self.__data: List[Dict[str, int]] = data
        self.__hline: str = "\t\t" + "-" * 40 + "\n"
        self.__hours: int = hours
        self.__opt: str = option
    
    def __str__(self) -> str:
        self.__MSG: str = f"🔗 The following table ranks the most active members in this {self.__opt} since the last {self.__hours} hours.\n\n\n"
        self.__MSG+= f"\t\t{"Top":^10}|{"Name":^15}|{"Messages":^15}\n"
        for ind, mb in enumerate(self.__data):
            self.__MSG += self.__hline
            self.__MSG += f"\t\t{(ind + 1):^10}|{get_max_str_size(list(mb.keys())[0]):^15}|{list(mb.values())[0]:^15}\n"
        self.__MSG += f"\nThis analysis considers the quantity of messages sent by the members inside this {self.__opt}"
        return f"""```{self.__MSG}```"""