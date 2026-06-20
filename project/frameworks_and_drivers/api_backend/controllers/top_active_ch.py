from flask_restful import abort, Resource
from typing import Dict, List
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from pprint import pprint
from project.interface_adapters.presenters.new_server_presenter import NewServerPresenter
from project.application.use_cases.new_server_use_case import NewServerUseCase
from project.frameworks_and_drivers.databases.mysql_db.dql.channel_dql import ChannelDQL
from flask import Response, request

class TopActiveCh(Resource):

    def get(self) -> Response:

        #Getting and checking the server_id
        self.__server_id: int | None = request.args.get("server_id", type = int)
        if self.__server_id is None:
            abort(400, message = "You must send the id of the server to \"server_id\"")
        
        #Querying the database
        self.__dataset: List[Dict[str, int]] = ChannelDQL().get_top_active_ch_from_db(self.__server_id)

        self.__resp: Dict[str, str | List[Dict[str, int]]] = {
            "message" : "ok",
            "data" : self.__dataset
        }  
        return self.__resp, 200