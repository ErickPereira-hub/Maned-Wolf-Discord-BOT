from flask import request
from flask_restful import abort
from project.frameworks_and_drivers.api_backend.jwt.jwt_singleton import JWT_SINGLETON
from typing import Any, Dict
import os

def is_authorized() -> int:

    #The cookie awlays come in the headers of the request.
    token: str = request.cookies.get(os.getenv("JWT_COOKIE_TAG"))

    #Checking the existence of the cookie
    if token is None:
        abort(401, message = "Not authorized: cookie isn't present or has expired")
    
    payload: Dict[str, Any] = JWT_SINGLETON.extract_payload(token)
    
    if payload is None: #<--- Remember: None means that the token has expired
        abort(401, message = "Not authorized: JWT token has expired")
    
    #If we get here, the user is authorized and we have access to the id of the user
    uid: int = payload["uid"]

    return uid #<--- Returning the id of the user