from typing import Dict, Tuple
from project.application.utils.date_conversion import get_date_in_EN

class MembersTable:

    def __init__(self, members_in_dataset: Dict[str, Tuple[int, int, int]], num_of_days: int):
        self.__members_in_ds: Dict[str, Tuple[int, int, int]] = members_in_dataset
        self.__num_of_days: int = num_of_days if num_of_days <= 10 else 10 #<--- Truncating the number to 10 if it is bigger than 10.
        self.__ds_len: int = len(members_in_dataset) #<--- Length of the dataset
        self.__first_pos: int = 0 if self.__ds_len < self.__num_of_days else self.__ds_len - self.__num_of_days
    
    def __str__(self) -> str:
        oavg, lavg = self.__get_avg_to_present()
        self.__repr: str = f"""
        🔗 Table of quantity of members for the last {self.__num_of_days} days:

            DAY            |{"Joined In":^13}|{"Deleted":^13}|{"Variation":^13}|{"Total":^13}
        ----------------------------------------------------------
        {("\n" + " "*8 + "-"*58 + "\n" + " "*8).join([f"{get_date_in_EN(day)} |{qtt[0]:^20}|{qtt[1]:^20}|{qtt[2]:^20}|{qtt[3]:^20}" for day, qtt in self.__members_in_ds.items()][self.__first_pos  : self.__ds_len])}

        Overall number of registered days: {len(self.__members_in_ds)}
        Overall average dailly throughput per day: {oavg:.2f}
        Average dailly throughput for the last {self.__num_of_days} days: {lavg:.2f}
        """
        return self.__repr
    
    def __get_avg_to_present(self) -> Tuple[float, float]:
        print(2)
        self.__ovar_avg: float = sum(var[2] for var in self.__members_in_ds.values()) / self.__ds_len #<--- Average qtt per day (Overall)
        self.__quotient_lvar_avg: int = self.__num_of_days if self.__num_of_days < self.__ds_len else self.__ds_len
        self.__lvar_avg: float = sum([var[2] for var in self.__members_in_ds.values()][self.__first_pos  : self.__ds_len]) / self.__quotient_lvar_avg #<--- Average qtt for recent days
        return self.__ovar_avg, self.__lvar_avg