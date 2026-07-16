from flask_restful import abort, Resource
from typing import Dict, List
from project.interface_adapters.presenters.new_server_presenter import NewServerPresenter
from project.application.use_cases.new_server_use_case import NewServerUseCase
from project.frameworks_and_drivers.databases.mysql_db.dql.channel_dql import ChannelDQL
from flask import Response, request
from project.frameworks_and_drivers.api_backend.middlewares.rate_blocker import rate_blocker
from project.frameworks_and_drivers.databases.redis_db.cache_aside.ca_for_top_active import CacheAsideTopActive
from project.frameworks_and_drivers.api_backend.controllers.extensions.check_server_extension import dismish_non_servers

class TopActiveCh(Resource):

    def get(self) -> Response:

        rate_blocker() #<--- Rate blocker

        #Getting and checking the server_id
        self.__server_id: int | None = request.args.get("server_id", type = int)
        if self.__server_id is None:
            abort(400, message = "You must send the id of the server to \"server_id\"")
        dismish_non_servers(self.__server_id)
        self.__dataset: List[Dict[str, int]] | None = None
        #Checking the existence of data in Redis
        redis_obj: CacheAsideTopActive = CacheAsideTopActive(server_id = self.__server_id)
        if redis_obj.exists_in_cache():
            self.__dataset = redis_obj.fetch_cache() #<--- Fetching the data in Redis because it exits in memory
        else:
            #Querying the database in disk
            self.__dataset = ChannelDQL().get_top_active_ch_from_db(self.__server_id)
            redis_obj.insert_into_cache(self.__dataset) #<--- Sending the data to the database

        self.__resp: Dict[str, str | List[Dict[str, int]]] = {
            "message" : "ok",
            "data" : self.__dataset
        }  
        
        return self.__resp, 200