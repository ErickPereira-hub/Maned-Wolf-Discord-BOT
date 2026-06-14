from flask_restful import abort, Resource
from typing import Any, Dict, Tuple
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_member import MemberDML

class Member(Resource):
    
    def post(self):
        self.__args: Dict[str, Any] = HTTP_BODY_ARGS.args_new_member.parse_args()
        #Checking if everything is ok with the message
        self.__important: Tuple[str] = ("member_id_disc", "server_id")
        for key in self.__important:
            if self.__args[key] is None:
                abort(400, message = "An important information about the server wasn't given")

        #Sending the member to the database
        MemberDML().send_to_db(
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