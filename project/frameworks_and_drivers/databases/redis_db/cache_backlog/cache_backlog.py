from project.frameworks_and_drivers.databases.redis_db.infra.redis_cnx_singleton import rcnx
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_backlog import BacklogDML
from typing import Dict
from datetime import datetime
from time import time, sleep

class CacheBacklog:

    KEY: str = "backlog"

    @classmethod
    def __reset_backlog(cls) -> None:
        cls.__first_info: Dict[str, int | str] = {
            "429" : 0, #<--- Quantity of Too Many Requests
            "qtt" : 0, #<--- Quantity of requests
            "fail" : 0, #<--- Quantity of requests different from 200 or 201, but in the range 400 to 499
            "ok" : 0, #<--- Quantity of requests that are 200 or 201 (I didn't work with others success codes)
            "500": 0, #<--- Quantity of 500 raised by the API
            "date": str(datetime.utcnow())
        }
        rcnx.hset(cls.KEY, mapping = cls.__first_info)

    @classmethod
    def __stringfy_info(cls, info: Dict[bytes, bytes]) -> Dict[str, str]:
        cls.__stringfied_info: Dict[str, str] = {}
        for info_key, info_val in info.items():
            cls.__stringfied_info.update({info_key.decode() : info_val.decode()})
        return cls.__stringfied_info

    @classmethod
    def update_backlog(cls, status_code: int) -> None:

        #Analyzing the status code
        is_429: bool = status_code == 429
        is_fail: bool = 400 <= status_code <= 499
        is_ok: bool = status_code in (200, 201)
        is_fatal: bool = status_code == 500

        cls.__str_info: Dict[str, str] | None = None #<--- informatino with strings

        if bool(rcnx.exists(cls.KEY)):

            #Grabbing the data from the RAM
            cls.__last_info: Dict[bytes, bytes] = rcnx.hgetall(cls.KEY)
            cls.__str_info = cls.__stringfy_info(cls.__last_info)

            #Setting the hash map
            rcnx.hset(cls.KEY, mapping = {
                "429": int(cls.__str_info["429"]) + 1 if is_429 else int(cls.__str_info["429"]),
                "500": int(cls.__str_info["500"]) + 1 if is_fatal else int(cls.__str_info["500"]),
                "qtt": int(cls.__str_info["qtt"]) + 1,
                "fail": int(cls.__str_info["fail"]) + 1 if is_fail else int(cls.__str_info["fail"]),
                "ok": int(cls.__str_info["ok"]) + 1 if is_ok else int(cls.__str_info["ok"]),
                "date": str(datetime.utcnow())
            })
        
        else:

            #Generating the data
            rcnx.hset(cls.KEY, mapping = {
                "429": 1 if is_429 else 0,
                "500": 1 if is_fatal else 0,
                "qtt": 1,
                "fail": 1 if is_fail else 0,
                "ok": 1 if is_ok else 0,
                "date": str(datetime.utcnow())
            })

    @classmethod
    def __send_to_disk(cls) -> None:
        cls.__binfo: Dict[bytes, bytes] = rcnx.hgetall(cls.KEY)
        cls.__info: Dict[str, str] = cls.__stringfy_info(cls.__binfo)
        BacklogDML().send_to_db(cls.__info)

    @classmethod
    def __show_backlog(cls) -> None:
        MSG: str = "="*80 + "\n"
        if bool(rcnx.exists(cls.KEY)):
            cls.__info: Dict[str, str] = cls.__stringfy_info(rcnx.hgetall(cls.KEY))
            MSG += f"\033[36mToo many requests >> {cls.__info["429"]}\033[m\n"
            MSG += f"\033[36mInternal server errors >> {cls.__info["500"]}\033[m\n"
            MSG += f"\033[36mFailures (4XX) >> {cls.__info["fail"]}\033[m\n"
            MSG += f"\033[36mQuantity >> {cls.__info["qtt"]}\033[m\n"
            MSG += f"\033[36mSuccess requests >> {cls.__info["ok"]}\033[m\n\n"
            MSG += f"\033[32mResults fetched from {cls.__info["date"]} to {datetime.utcnow()}\033[m\n"
        else:
            MSG += "No requests"
        print(MSG)

    @classmethod
    def process_backlogs(cls) -> None:
        #Sending the metrics to the database for each minute
        while True:
            t_start: float = time()
            cls.__show_backlog()
            if bool(rcnx.exists(cls.KEY)):
                cls.__send_to_disk()
                cls.__reset_backlog() #<--- Reseting the metrics from 0
            t_end: float = time()
            t_interval: float = t_end - t_start
            sleep(60 - t_interval)