from flask_restful import abort, Resource
from flask import Response, make_response
from typing import Any, Dict
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from project.frameworks_and_drivers.databases.mysql_db.dql.server_dql import ServerDQL
from flask import Response
from project.frameworks_and_drivers.api_backend.controllers.extensions.pull_data_extension import pull_data_ext
from project.frameworks_and_drivers.api_backend.jwt.jwt_singleton import JWT_SINGLETON
from project.frameworks_and_drivers.api_backend.middlewares.cookies_middleware import send_cookie
import os
import json
from project.frameworks_and_drivers.api_backend.middlewares.block_brute_force_attacks import block_brute_force_attacks
from project.frameworks_and_drivers.databases.redis_db.rate_limit.block_login_abuse import loginBlocker

class PullBigData(Resource):

    def post(self) -> Response:

        #Catching the json with the token access
        self.__JSON: Dict[str, str] = HTTP_BODY_ARGS.server_token.parse_args()
        self.__token: str = self.__JSON["token"]
        self.__sid: int = self.__JSON["sid"]
        
        #Discarding empty token
        if self.__token == "":
            abort(422, message = "Token can't be empty")

        #Discarding non-sense id
        if self.__sid < 0:
            abort(422, message = "Id can't be negative")

        block_brute_force_attacks(self.__sid) #<--- Blocking brute force attacks

        self.__signal: bool = ServerDQL().has_permission(
            sid = self.__sid,
            token = self.__token
        )

        if self.__signal:
            self.__resp: Dict[str, Any] = pull_data_ext(self.__sid)
            self.__jwt_token: str = JWT_SINGLETON.get_new_jwt_token(self.__sid)
            self.__legit_response: Response = make_response(json.dumps(self.__resp), 200)
            self.__legit_response.headers["Content-Type"] = "application/json"
            loginBlocker.delete_user(self.__sid) #<--- Deleting the user from redis for the brute force analysis
            send_cookie(
                resp = self.__legit_response,
                key = os.getenv("JWT_COOKIE_TAG"),
                data = self.__jwt_token
                )
            return self.__legit_response

        return {"message": "User doesn't have permission"}, 401