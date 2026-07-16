from flask_restful import abort, Resource
from typing import Dict, List, Tuple
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from flask import Response, request
from project.frameworks_and_drivers.api_backend.middlewares.rate_blocker import rate_blocker
from project.frameworks_and_drivers.api_backend.controllers.extensions.check_server_extension import dismish_non_servers

class TopMembers(Resource):

    def get(self) -> Response:

        rate_blocker() #<--- Rate blocker

        #Catching and checking the id of the server, channel
        self.__sid: int | None = request.args.get("server_id", type = int)
        self.__cid: int | None = request.args.get("channel_id", type = int)
        self.__from_date: str | None = request.args.get("from_date", type = str)
        self.__by: str | None = request.args.get("by", type = str)
        self.__creds: Tuple[int | None, int | None, str | None, str | None] = (self.__sid, self.__cid, self.__from_date, self.__by)
        for cred in self.__creds:
            if cred is None:
                abort(400, message = f"\'{cred}\' must be filled")
        if self.__by not in ("channel", "server"):
            abort(400, message = "\'channel\' and \'server\' are the unique possible values for the parameter \'by\'")
        dismish_non_servers(self.__sid)
        self.__data: List[Dict[str, int]] | None = None #<--- Future JSON response

        #If the user wants to catch the most active members by channel:
        if self.__by == "channel":
            self.__data = MemberDQL().get_active_members_on_channel_from_db(
                    cid = self.__cid,
                    sid = self.__sid,
                    from_date = self.__from_date)
            return self.__data, 200
        
        #If the user wants to catch the most active members by server, not channel:
        if self.__by == "server":
            self.__data = MemberDQL().get_active_members_on_server_from_db(
                    sid = self.__sid,
                    from_date = self.__from_date)
            return self.__data, 200