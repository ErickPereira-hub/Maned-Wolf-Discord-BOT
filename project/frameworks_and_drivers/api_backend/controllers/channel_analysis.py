from flask_restful import abort, Resource
from typing import Dict
from project.frameworks_and_drivers.databases.mysql_db.dql.channel_dql import ChannelDQL
from flask import request, Response
from project.frameworks_and_drivers.api_backend.middlewares.rate_blocker import rate_blocker

class ChannelAnalysis(Resource):

    def get(self) -> Response:

        rate_blocker() #<--- Rate blocker

        #Getting the id of the server and the requested style
        self.__sid: int | None = request.args.get("server_id", type = int)
        self.__style: int | None = request.args.get("style", type = str)

        #Checking incoming data
        if self.__sid is None:
            abort(400, message = "server_id must be given")
        if self.__style is None or self.__style not in ("nsfw", "category"):
            abort(400, message = "style must be given and it must be \'nsfw\' or \'category\'")

        self.__data: Dict[str, int] | None = None #<--- Declaring the attribute that will receive the data from the database

        #Fetching the database
        if self.__style == "category":
            self.__data = ChannelDQL().get_ch_cat_from_db(self.__sid)
        else:
            self.__data = ChannelDQL().get_ch_nsfw_from_db(self.__sid)

        #Preparing the response
        self.__resp: Dict[str, Dict[str, int] | str] = {
            "message" : "ok",
            "data" : self.__data
        }

        return self.__resp, 200