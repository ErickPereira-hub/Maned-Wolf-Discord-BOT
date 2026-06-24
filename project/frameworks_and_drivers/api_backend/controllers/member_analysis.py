from flask_restful import abort, Resource
from typing import Dict, Tuple
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from flask import request, Response
from project.frameworks_and_drivers.api_backend.middlewares.acumulative_freq_middleware import add_acum_freq_middleware
from project.frameworks_and_drivers.api_backend.middlewares.rate_blocker import rate_blocker
from project.frameworks_and_drivers.databases.redis_db.cache_aside.ca_for_member_analysis import CacheAsideMemberAnalysis

class MemberAnaysis(Resource):

    def __init__(self):
        super().__init__()
        self.__MEMBER_DQL_SINGLETON: MemberDQL = MemberDQL()

    def get(self) -> Response:

        rate_blocker() #<--- Rate blocker
        
        self.__server_id: int | None = request.args.get("server_id", type = int)

        #Checking the server_id
        if self.__server_id is None:
            abort(400, message = "The server id wasn't given")
        
        self.__data: Dict[str, Tuple[int, int, int]] | None = None

        #Applying cache-aside and fetching the database
        self.__cache_obj: CacheAsideMemberAnalysis = CacheAsideMemberAnalysis(server_id = self.__server_id)
        if self.__cache_obj.exists_in_cache():
            self.__data = self.__cache_obj.fetch_cache()
        else:
            self.__data = self.__MEMBER_DQL_SINGLETON.get_members_qtt(server_id = self.__server_id)
            self.__cache_obj.insert_into_cache(JSON = self.__data)
        print(self.__data)
        #Grabbing the quantities of members for each day
        self.__complete_data: Dict[str, Tuple[int, int, int, int]] = add_acum_freq_middleware(self.__data)
        
        return self.__complete_data, 200