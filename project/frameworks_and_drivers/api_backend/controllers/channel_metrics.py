from flask_restful import abort, Resource
from typing import Dict
from project.frameworks_and_drivers.databases.mysql_db.dql.channel_dql import ChannelDQL
from flask import request, Response

class ChannelMetrics(Resource):

    def get(self) -> Response:

        #Getting the id of the server
        self.__sid: int | None = request.args.get("server_id", type = int)
        if self.__sid is None:
            abort(400, message = "server_id must be given")
        
        #Fetching the database
        self.__data: Dict[str, Dict[str, int]] = ChannelDQL().get_ch_metrics_from_db(self.__sid)
        
        #Preparing the response
        self.__resp: Dict[str, Dict[str, Dict[str, int]] | str] = {
            "message" : "ok",
            "data" : self.__data
        }

        return self.__resp, 200