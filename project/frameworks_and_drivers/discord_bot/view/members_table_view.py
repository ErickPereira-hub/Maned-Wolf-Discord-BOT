from typing import Dict, Tuple
from project.application.utils.date_conversion import get_date_in_EN

class MembersQttView:

    def __init__(self,
                members_in_dataset: Dict[str, Tuple[int, int, int, int]],
                num_of_days: int,
                overall_tot_avg: float,
                overall_tot_std_dev: float,
                overall_var_avg: float,
                overall_var_std_dev: float):
        self.__members_in_ds: Dict[str, Tuple[int, int, int, int]] = members_in_dataset
        self.__num_of_days: int = num_of_days if num_of_days <= 7 else 7 #<--- Truncating the number to 7 if it is bigger than 7. It avoids a problem of character limit in discord.
        self.__ds_len: int = len(members_in_dataset) #<--- Length of the dataset (Numbers of analysed days from the first contact of a member with the server until today)
        self.__first_pos: int = 0 if self.__ds_len < self.__num_of_days else self.__ds_len - self.__num_of_days
        self.__overall_tot_avg: float = overall_tot_avg
        self.__overall_tot_std_dev: float = overall_tot_std_dev
        self.__overall_var_avg: float = overall_var_avg
        self.__overall_var_std_dev: float = overall_var_std_dev
    
    def __str__(self) -> str:
        self.__repr: str = f"""```\n
        🔗 Table of quantity of members for the last {self.__num_of_days} days:

        {"Day":^11}|{"Joined In":^13}|{"Deleted":^13}|{"Variation":^13}|{"Total":^11}
        ---------------------------------------------------------------
        {("\n" + " "*8 + "-"*63 + "\n" + " "*8).join([f"{get_date_in_EN(day)} |{qtt[0]:^13}|{qtt[1]:^13}|{qtt[2]:^13}|{qtt[3]:^13}" for day, qtt in self.__members_in_ds.items()][self.__first_pos  : self.__ds_len])}

        {self.get_desc()}

        {self.__present_incr(self.__get_avg_to_present()[1], self.__overall_tot_avg)}

```"""
        return self.__repr
    
    def __get_avg_to_present(self) -> Tuple[float, float]:
        self.__quotient: int = self.__num_of_days if self.__num_of_days < self.__ds_len else self.__ds_len#<--- Size of the shown data
        self.__rvar_avg: float = sum([var[2] for var in self.__members_in_ds.values()][self.__first_pos : self.__ds_len]) / self.__quotient #<--- Average variation for recent days
        self.__rtot_avg: float = sum([var[3] for var in self.__members_in_ds.values()][self.__first_pos : self.__ds_len]) / self.__quotient #<--- Average variation for recent days
        return self.__rvar_avg, self.__rtot_avg
    
    def __get_incr(self, avg_tot_recent: float, avg_tot_overall: float) -> float | None:
        if self.__ds_len <= self.__num_of_days:
            return None
        incr: float = 100 * (avg_tot_recent / avg_tot_overall) - 100
        return incr
    
    def __present_incr(self, avg_tot_recent: float, avg_tot_overall: float) -> str:
        incr_resp: None | float = self.__get_incr(avg_tot_recent, avg_tot_overall)
        
        if incr_resp is None:
            return ""

        PREVIEW: str = "Total of members of recent days compared with overall results: "

        if incr_resp < 0:
            return PREVIEW + f"Decrease of {incr_resp:.2f}%"
        
        if incr_resp >= 0:
            return PREVIEW + f"Increase of {incr_resp:.2f}%"
    
    def get_desc(self, into_embed: bool = False) -> str:
        r_var_avg, r_tot_avg = self.__get_avg_to_present()
        return f"""
        {"(*)" if not into_embed else "📑 "} Overall information:\n
        {f"Number of registered days: {self.__ds_len}":<}
        {f"Average dailly variation: {self.__overall_var_avg:.2f}":<45}{"\n" if into_embed else ""}{f"Overall standard deviation for daily variation: {self.__overall_var_std_dev:.2f}":>45}
        {f"Average total of members for each day: {self.__overall_tot_avg:.2f}":<45}{"\n" if into_embed else ""}{f"Overall standard deviation for daily total: {self.__overall_tot_std_dev:.2f}":>45}
        \n
        {"(*)" if not into_embed else "📑 "} Information for the last {self.__num_of_days} days:\n
        Average dailly variation for the last {self.__num_of_days} days: {r_var_avg:.2f}
        Average dailly total of members for the last {self.__num_of_days} days: {r_tot_avg:.2f}
"""