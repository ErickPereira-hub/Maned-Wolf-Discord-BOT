from typing import List, Dict
from project.application.utils.max_str_size import get_max_str_size

class GetTopActiveChannelsView:

    def __init__(self, data: List[Dict[str, int]]):
        self.__data: List[Dict[str, int]] = data
        self.__hline: str = "\t\t" + "-" * 40 + "\n"
    
    def __str__(self) -> str:
        self.__MSG: str = "🔗 The following table ranks the text channels with the most message volume since this bot was integrated with this server.\n\n\n"
        self.__MSG+= f"\t\t{"Top":^10}|{"Channel name":^15}|{"Messages":^15}\n"
        for ind, ch in enumerate(self.__data):
            self.__MSG += self.__hline
            self.__MSG += f"\t\t{(ind + 1):^10}|{get_max_str_size(list(ch.keys())[0]):^15}|{list(ch.values())[0]:^15}\n"
        return f"""```{self.__MSG}```"""