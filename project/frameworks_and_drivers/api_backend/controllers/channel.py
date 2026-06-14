from flask_restful import abort, Resource
from typing import Any, Dict, Tuple
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_channel import ChannelDML

class Channel(Resource):
    
    def post(self):
        #Grabbing the data from the discord endpoint
        self.__args: Dict[str, Any] = HTTP_BODY_ARGS.args_new_channel.parse_args()
        #Checking if everything is ok with the message
        self.__important: Tuple[str] = ("channel_id", "server_id")
        for key in self.__important:
            if self.__args[key] is None:
                abort(400, message = "An important information about the server wasn't given")

        #Sending the channel to the database
        ChannelDML().send_to_db(
            channel_id = self.__args["channel_id"],
            channel_name = self.__args["channel_name"],
            category = self.__args["category"],
            is_nsfw = self.__args["is_nsfw"],
            server_id = self.__args["server_id"]
        )
        
        #Must run if everything went well
        self.__GOOD_JSON_RESPONSE: Dict[str, str] = {"status": "Ok", "message": f"Channel {self.__args["channel_name"]} has been added!"}
        return self.__GOOD_JSON_RESPONSE, 201