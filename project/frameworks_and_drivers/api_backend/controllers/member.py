from flask_restful import abort, Resource
from typing import Any, Dict, Tuple
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_member import MemberDML
from flask import request, Response
from project.frameworks_and_drivers.api_backend.controllers.extensions.check_server_extension import dismish_non_servers

class Member(Resource):
    
    def __init__(self):
        super().__init__()
        self.__MEMBER_DB_OBJ: MemberDML = MemberDML()

    def post(self) -> Response:
        self.__args: Dict[str, Any] = HTTP_BODY_ARGS.args_new_member.parse_args()
        #Checking if everything is ok with the message
        self.__important: Tuple[str] = ("member_id_disc", "server_id")
        for key in self.__important:
            if self.__args[key] is None:
                abort(400, message = "An important information about the server wasn't given")
        dismish_non_servers(self.__args["server_id"])
        
        #Sending the member to the database
        self.__MEMBER_DB_OBJ.send_to_db(
            member_id_disc = self.__args["member_id_disc"],
            member_name = self.__args["member_name"],
            category = self.__args["category"],
            joined_at = self.__args["joined_at"],
            account_create_at = self.__args["account_create_at"],
            server_id = self.__args["server_id"]
        )
        
        #Must run if everything went well
        self.__GOOD_JSON_RESPONSE: Dict[str, str] = {"status": "Ok", "message": f"Member {self.__args["member_name"]} joined in"}
        return self.__GOOD_JSON_RESPONSE, 201

    def delete(self) -> Response:
        self.__member_id: int | None = request.args.get("member_id", type = int)
        self.__server_id: int | None = request.args.get("server_id", type = int)
        #Checking the id
        if self.__member_id is None and self.__server_id is None:
            return {"message": "You must deliver an id inside the 'member_id' and 'server_id' in the URL"}, 400
        #Deleting the data
        self.__MEMBER_DB_OBJ.del_in_db(self.__member_id, self.__server_id)
        return {"message": f"Member of id {self.__member_id} has been successfully deleted"}, 200