from flask import request, Response
import os
from project.frameworks_and_drivers.api_backend.jwt.jwt_singleton import JWT_SINGLETON
from project.frameworks_and_drivers.api_backend.middlewares.cookies_middleware import send_cookie

def refresh_jwt_or_cookie(resp: Response) -> None:

    #Getting the cookie
    jwt_token: str = request.cookies.get(os.getenv("JWT_COOKIE_TAG"))

    #Refreshing the jwt token if needed
    new_jwt_token: str | None = JWT_SINGLETON.get_refreshed_jwt_token(jwt_token)

    #Refreshing the cookie with the new JWT and the cookie TTL
    send_cookie(
        resp = resp,
        key = os.getenv("JWT_COOKIE_TAG"),
        data = new_jwt_token)