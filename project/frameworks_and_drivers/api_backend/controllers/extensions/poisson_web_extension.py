from flask import request
from flask_restful import abort
from project.frameworks_and_drivers.api_backend.middlewares.auth_middleware import is_authorized
from typing import Dict

def get_poisson_web_beginning() -> Dict[str, int]:

    #Checking authorization
    uid: int = is_authorized()
    
    #Grabbing the range of analysis
    _from: int | None = request.args.get("from", type = int)
    until: int | None = request.args.get("until", type = int)
    
    #Checking the income values
    if _from is None or until is None:
        abort(400, message = "Bad Request: you must deliver integers to 'from' and 'until' parameters")
    
    #Ignoring invalid values
    if _from < 0 or _from > until:
        abort(422, message = "Forbidden values: 'from' must be positive and can't be lower than 'until'")

    data: Dict[str, int] = {
        "from" : _from,
        "until" : until,
        "uid" : uid
    }

    return data