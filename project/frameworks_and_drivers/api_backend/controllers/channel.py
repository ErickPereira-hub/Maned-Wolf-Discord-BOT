from flask_restful import abort, Resource
from typing import Any, Dict, Tuple
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_channel import ChannelDML
from flask import request

class Channel(Resource):
    
    def __init__(self):
        super().__init__()
        self.__CHANNEL_DB_OBJ: ChannelDML = ChannelDML()

    def post(self):
        #Grabbing the data from the discord endpoint
        self.__args: Dict[str, Any] = HTTP_BODY_ARGS.args_new_channel.parse_args()
        #Checking if everything is ok with the message
        self.__important: Tuple[str] = ("channel_id", "server_id")
        for key in self.__important:
            if self.__args[key] is None:
                abort(400, message = "An important information about the server wasn't given")

        #Sending the channel to the database
        self.__CHANNEL_DB_OBJ.send_to_db(
            channel_id = self.__args["channel_id"],
            channel_name = self.__args["channel_name"],
            category = self.__args["category"],
            is_nsfw = self.__args["is_nsfw"],
            server_id = self.__args["server_id"]
        )
        
        #Must run if everything went well
        self.__GOOD_JSON_RESPONSE: Dict[str, str] = {"status": "Ok", "message": f"Channel {self.__args["channel_name"]} has been added!"}
        return self.__GOOD_JSON_RESPONSE, 201
    
    def delete(self):
        self.__cid: int | None = request.args.get("channel_id", type = int)
        #Checking if the id came
        if self.__cid is None:
            return {"message": f"ERROR ---> You must give the id of the channel"}, 400
        self.__CHANNEL_DB_OBJ.del_in_db(self.__cid)
        return {"message": f"Channel of id {self.__cid} has been deleted"}, 200
    
    def patch(self):
        #Capturing the data from the new version of the channel
        self.__cid: int | None = request.args.get("channel_id", type = int)
        self.__new_name: str | None = request.args.get("new_name", type = str)
        self.__new_category: str | None = request.args.get("new_category", type = str)
        self.__new_is_nsfw: str | None = request.args.get("new_is_nsfw", type = str)
        
        #Checking if the id is None
        if self.__cid is None:
            return {"message": "ERROR ---> The channel id that went to the api is None"}, 400

        #Updating the data in the database
        self.__CHANNEL_DB_OBJ.update_in_db(
            cid = self.__cid,
            new_name = self.__new_name,
            new_category = self.__new_category,
            new_is_nsfw = self.__new_is_nsfw
        )
        return {"message": "ok"}, 200