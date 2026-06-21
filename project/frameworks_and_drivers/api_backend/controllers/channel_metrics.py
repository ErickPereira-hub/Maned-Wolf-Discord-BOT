from flask_restful import abort, Resource
from typing import Dict
from project.frameworks_and_drivers.databases.mysql_db.dql.channel_dql import ChannelDQL
from flask import request, Response

class ChannelMetrics(Resource):

    def get(self) -> Response:

        #Getting the id of the server
        self.__sid: int | None = request.args.get("server_id", type = int)
        self.__style: int | None = request.args.get("style", type = str)
        if self.__sid is None:
            abort(400, message = "server_id must be given")
        print(self.__style)
        if self.__style is None or self.__style not in ("nsfw", "category"):
            abort(400, message = "type must be given ('nsfw' or 'category')")
        
        self.__data: Dict[str, int] | None = None

        #Fetching the database
        if self.__style == "category":
            self.__data = ChannelDQL().get_ch_cat_from_db(self.__sid)
        else:
            self.__data = ChannelDQL().get_ch_nsfw_from_db(self.__sid)
        
        #Preparing the response
        self.__resp: Dict[str, Dict[str, Dict[str, int]] | str] = {
            "message" : "ok",
            "data" : self.__data
        }

        return self.__resp, 200