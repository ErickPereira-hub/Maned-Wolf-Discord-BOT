from flask_restful import reqparse
from project.application.utils.func_type_list import list_str, list_int
from typing import Any, Dict

class HttpRequestBodyArgs:

    STD_HELP_MSG: str = "Trouble with an argument"

    def __init__(self):
        #Setting the standard JSON for new server
        self.__ARGS_NEW_SERVER: reqparse.RequestParser = reqparse.RequestParser()
        self.__load_new_server_json()
    
    def __load_new_server_json(self) -> None:
        self.__info_to_load: Dict[str, Any] = {
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
            "types": list_str,
            "ccategories": list_str,
            "are_nsfw": list_str,
            "members_id": list_int,
            "channels_id": list_int,
        }
        for field, type in self.__info_to_load.items():
            self.__ARGS_NEW_SERVER.add_argument(field, type = type, location = "json", help = HttpRequestBodyArgs.STD_HELP_MSG, required = True)
        
        """self.__ARGS_NEW_SERVER.add_argument("server_id", type = int, help = HttpRequestBodyArgs.STD_HELP_MSG, required = True)
        self.__ARGS_NEW_SERVER.add_argument("server_name", type = str, help = HttpRequestBodyArgs.STD_HELP_MSG)
        self.__ARGS_NEW_SERVER.add_argument("description", type = str, help = HttpRequestBodyArgs.STD_HELP_MSG)
        self.__ARGS_NEW_SERVER.add_argument("owner_name", type = str, help = HttpRequestBodyArgs.STD_HELP_MSG)
        self.__ARGS_NEW_SERVER.add_argument("server_creation_date", type = str, help = HttpRequestBodyArgs.STD_HELP_MSG)
        for fn in (
            "members_name",
            "mcategories",
            "they_joined_at",
            "their_account_were_create_at",
            "channels_name",
            "types",
            "ccategories",
            "are_nsfw"):
            self.__ARGS_NEW_SERVER.add_argument(fn, type = list_str, location = "json", help = HttpRequestBodyArgs.STD_HELP_MSG)
        for fn in (
            "members_id",
            "channels_id",
        ):
            self.__ARGS_NEW_SERVER.add_argument(fn, type = list_int, location = "json", help = HttpRequestBodyArgs.STD_HELP_MSG)"""

    @property
    def args_new_server(self) -> reqparse.RequestParser:
        return self.__ARGS_NEW_SERVER