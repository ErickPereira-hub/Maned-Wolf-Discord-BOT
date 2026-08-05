from flask import Response, request, make_response
from flask_restful import Resource, abort
from project.frameworks_and_drivers.api_backend.middlewares.refresh_cookie import refresh_jwt_or_cookie
from project.frameworks_and_drivers.api_backend.middlewares.auth_middleware import is_authorized
from project.frameworks_and_drivers.databases.mysql_db.dql.messages_dql import MessageDQL
import os

class LogOut(Resource):

    def delete(self):
        self.__resp: Response = make_response({"message" : "deleted"}, 200)
        self.__resp.delete_cookie(
            os.getenv("JWT_COOKIE_TAG"),
            httponly = True,
            secure = True,
            samesite = "none"
            ) #<--- Requesting imediate deletion of the cookie in the browser.
        return self.__resp