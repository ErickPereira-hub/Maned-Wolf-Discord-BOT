from flask_restful import reqparse
from project.application.utils.func_type_list import list_str, list_int
from typing import Any, Dict

class HttpRequestBodyArgs:

    STD_HELP_MSG: str = "Trouble with an argument"

    def __init__(self):
        #Setting the standard JSON for new server
        self.__ARGS_NEW_SERVER: reqparse.RequestParser = reqparse.RequestParser()
        self.__ARGS_NEW_MSG: reqparse.RequestParser = reqparse.RequestParser()
        self.__load_new_server_json({
            "server_id": int,
            "server_name": str,
            "description": str,
            "owner_name": str,
            "server_creation_date": str,
            "members_name": list_str,
            "mcategories": list_str,
            "they_joined_at": list_str,
            "their_account_were_create_at": list_str,
            "channels_name": list_str,
            "ccategories": list_str,
            "are_nsfw": list_str,
            "members_id": list_int,
            "channels_id": list_int,
        })
        self.__load_new_msg_json({
            "msg_id" : int,
            "msg_text" : str,
            "msg_date" : str,
            "msg_edited_at" : str,
            "author_id" : int,
            "channel_id" : int,
            "server_id" : int
        })
    
    def __load_new_server_json(self, info: Dict[str, Any]) -> None:
        for field, type in info.items():
            self.__ARGS_NEW_SERVER.add_argument(field, type = type, location = "json", help = HttpRequestBodyArgs.STD_HELP_MSG, required = True)
     
    def __load_new_msg_json(self, info: Dict[str, Any]) -> None:
        for field, type in info.items():
            self.__ARGS_NEW_MSG.add_argument(field, type = type, help = HttpRequestBodyArgs.STD_HELP_MSG, required = True)

    @property
    def args_new_server(self) -> reqparse.RequestParser:
        return self.__ARGS_NEW_SERVER
    
    @property
    def args_new_msg(self) -> reqparse.RequestParser:
        return self.__ARGS_NEW_MSG