from typing import Any
from project.frameworks_and_drivers.databases.redis_db.infra.redis_cnx_singleton import rcnx
import json
import os

class CacheAside:

    def insert_into_cache(self, JSON: Any) -> None:
        print("inserted")
        rcnx.set(self.key, json.dumps(JSON)) #<--- Loading the JSON is redis as a string
        rcnx.expire(self.key, os.getenv("CA_EXP_TIME"))
    
    def fetch_cache(self) -> Any:
        print("fetched")
        self.__JSON: Any = json.loads(rcnx.get(self.key).decode())
        return self.__JSON
    
    def exists_in_cache(self) -> bool:
        return bool(rcnx.exists(self.key))