from flask import Response, make_response
from flask_restful import Resource
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