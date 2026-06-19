from project.application.utils.date_conversion import get_date_in_EN
from datetime import timedelta
from datetime import datetime
from typing import Dict, Any

class ViewPredictMembersQttBetween:

    def __init__(self, day: int, show_poly: str, resp: Dict[str, Any], latency: float):
        self.__day: int = day
        self.__show_poly: str = show_poly
        self.__resp: Dict[str, Any] = resp
        self.__latency: float = latency
    
    def __str__(self) -> str:
        self.__day_t: str = self.__export_day(datetime.utcnow() + timedelta(days = self.__day))
        self.__err: float | int = self.__resp["error"]
        msg: str = f"🔗 Predicted total of members for day {self.__day_t}: {self.__resp["result"]:.2f} members"
        msg += f"\n\nError concerning the data: {self.__err:.2f}%" 
        if self.__show_poly == "show":
            msg += f"\n\nBest polynomial acquired: {self.__resp["poly"]}"
        msg += "\n\nReliability of the prediction:"

        if self.__err < 5:
            msg += "  ✅ almost infalible"
        elif self.__err < 20:
            msg += "  🔎 consistent"
        else:
            msg += "  ⚠️ Untrustable"
        
        msg += f"\n\nBackend Latency: {self.__latency:.4f} sec"
        return msg

    def __export_day(self, datetime: datetime) -> str:
        self.__day: str = str(datetime)[:10]
        self.__date_EN_str: str = get_date_in_EN(self.__day)
        return self.__date_EN_str