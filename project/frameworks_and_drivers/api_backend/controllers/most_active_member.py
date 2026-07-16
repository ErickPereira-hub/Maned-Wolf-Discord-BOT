from flask_restful import abort, Resource
from typing import Dict
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from flask import Response, request
from project.frameworks_and_drivers.api_backend.controllers.extensions.check_server_extension import dismish_non_servers

class MostActiveMember(Resource):

    def __init__(self):
        super().__init__()
        self.__most_active_id: int | None = None

    def get(self) -> Response:

        #Grabbing the important data from the discord endpoint
        self.__sid: int | None = request.args.get("server_id", type = int)
        self.__fd: str | None = request.args.get("from_date", type = str)
        
        #Checking
        if self.__sid is None or self.__fd is None:
            abort(400, message = "\'server_id\' and \'from_date\' must be informed")
        dismish_non_servers(self.__sid)
        #Invoking the id
        self.__most_active_id: int = MemberDQL().get_most_active_member_from_db(self.__sid, self.__fd)
        
        #Preparing the final response
        self.__final_resp: Dict[str, int] = {'id' : self.__most_active_id}
        
        return self.__final_resp, 200 #<--- Sending the response to the endpoint