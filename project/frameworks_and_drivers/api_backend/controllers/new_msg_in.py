from flask_restful import abort, Resource
from typing import Any, Dict, Tuple
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_msg import MessageDML

class NewMsgIn(Resource):
    
    def post(self):
        self.__args: Dict[str, Any] = HTTP_BODY_ARGS.args_new_msg.parse_args()
        #Checking if everything is ok with the message
        self.__important: Tuple[str] = ("msg_id", "author_id", "channel_id", "server_id")
        for key in self.__important:
            if self.__args[key] is None:
                abort(400, message = "An important information about the server wasn't given")
        
        #Sending the dataset to the database
        MessageDML().send_to_db(
            msg_id = self.__args["msg_id"],
            msg_txt = self.__args["msg_text"],
            msg_date = self.__args["msg_date"],
            msg_edited_at = self.__args["msg_edited_at"],
            author_id = self.__args["author_id"],
            channel_id = self.__args["channel_id"],
            server_id = self.__args["server_id"]
        )

        #Must run if everything went well
        self.__GOOD_JSON_RESPONSE: Dict[str, str] = {"message": "Ok"}
        return self.__GOOD_JSON_RESPONSE, 201