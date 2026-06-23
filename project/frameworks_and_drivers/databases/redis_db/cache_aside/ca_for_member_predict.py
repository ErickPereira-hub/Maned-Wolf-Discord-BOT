from typing import Dict, Tuple
from project.domain.interfaces.cache_aside import CacheAside
from project.frameworks_and_drivers.databases.redis_db.infra.redis_cnx_singleton import rcnx
import json
import os

class CacheAsideMemberPredict(CacheAside):

    def __init__(self, server_id: int):
        self.__key: str = f"ca_member_predict_{server_id}"

    def insert_into_cache(self, JSON: Dict[str, Tuple[int, int, int]]) -> None:
        rcnx.set(self.__key, json.dumps(JSON)) #<--- Loading the JSON inside redis as a string
        rcnx.expire(self.__key, os.getenv("CA_EXP_TIME"))
    
    def fetch_cache(self) -> Dict[str, Tuple[int, int, int]]:
        self.__JSON: Dict[str, Tuple[int, int, int]] = json.loads(rcnx.get(self.__key).decode())
        return self.__JSON
    
    def exists_in_cache(self) -> bool:
        return bool(rcnx.exists(self.__key))