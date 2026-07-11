from flask_restful import abort, Resource
from typing import Any, Dict
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from project.frameworks_and_drivers.databases.mysql_db.dql.server_dql import ServerDQL
from flask import Response
from project.frameworks_and_drivers.api_backend.middlewares.rate_blocker import rate_blocker
from project.frameworks_and_drivers.api_backend.controllers.pull_data_extension import pull_data_ext

class PullBigData(Resource):

    def post(self) -> Response:

        #Catching the json with the token access
        self.__JSON: Dict[str, str] = HTTP_BODY_ARGS.server_token.parse_args()
        self.__token: str = self.__JSON["token"]
        self.__sid: int = self.__JSON["sid"]
        print(1, flush = True)
        #Discarding empty token
        if self.__token == "":
            abort(422, message = "Token can't be empty")

        #Discarding non-sense id
        if self.__sid < 0:
            abort(422, message = "Id can't be negative")

        self.__signal: bool = ServerDQL().has_permission(
            sid = self.__sid,
            token = self.__token
        )

        if self.__signal:
            self.__resp: Dict[str, Any] = pull_data_ext(self.__sid)
            return self.__resp, 200

        return {"message": "User doesn't have permission"}, 401