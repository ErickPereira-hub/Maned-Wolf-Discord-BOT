from typing import Dict, List
from project.domain.interfaces.cache_aside import CacheAside
from project.frameworks_and_drivers.databases.redis_db.infra.redis_cnx_singleton import rcnx
import json
import os

class CacheAsideTopActive(CacheAside):

    def __init__(self, server_id: int):
        self.__key: str = f"ca_top_active_{server_id}"

    def insert_into_cache(self, JSON: List[Dict[str, int]]) -> None:
        rcnx.set(self.__key, json.dumps(JSON)) #<--- Loading the JSON is redis as a string
        rcnx.expire(self.__key, os.getenv("CA_EXP_TIME"))
    
    def fetch_cache(self) -> Dict[str, int]:
        self.__JSON: List[Dict[str, int]] = json.loads(rcnx.get(self.__key).decode())
        return self.__JSON
    
    def exists_in_cache(self) -> bool:
        return bool(rcnx.exists(self.__key))