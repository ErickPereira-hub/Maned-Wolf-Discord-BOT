from flask_restful import abort, Resource
from typing import Dict
from project.frameworks_and_drivers.databases.mysql_db.dql.channel_dql import ChannelDQL
from flask import request, Response
from project.frameworks_and_drivers.api_backend.middlewares.rate_blocker import rate_blocker
from project.frameworks_and_drivers.databases.redis_db.cache_aside.cache_aside import CacheAside
from project.frameworks_and_drivers.databases.redis_db.cache_aside.ca_for_ch_analysis_by_nsfw import CacheAsideChannelAnalysisByNSFW

class ChannelAnalysis(Resource):

    def get(self) -> Response:

        rate_blocker() #<--- Rate blocker

        #Getting the id of the server and the requested style
        self.__sid: int | None = request.args.get("server_id", type = int)

        #Checking incoming data
        if self.__sid is None:
            abort(400, message = "server_id must be given")

        self.__data: Dict[str, int] | None = None #<--- Declaring the attribute that will receive the data from the database

        ca_nsfw: CacheAside = CacheAsideChannelAnalysisByNSFW(self.__sid)
        if ca_nsfw.exists_in_cache():
            self.__data = ca_nsfw.fetch_cache()
        else:
            self.__data = ChannelDQL().get_ch_nsfw_from_db(self.__sid)
            ca_nsfw.insert_into_cache(JSON = self.__data)

        #Preparing the response
        self.__resp: Dict[str, Dict[str, int] | str] = {
            "message" : "ok",
            "data" : self.__data
        }

        return self.__resp, 200