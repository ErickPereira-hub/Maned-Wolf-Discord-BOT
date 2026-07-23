from flask import Response, request, make_response
from flask_restful import Resource, abort
from project.frameworks_and_drivers.api_backend.middlewares.refresh_cookie import refresh_jwt_or_cookie
from project.frameworks_and_drivers.api_backend.middlewares.auth_middleware import is_authorized
from project.frameworks_and_drivers.databases.mysql_db.dql.messages_dql import MessageDQL
from typing import Dict, List
from project.application.poisson_member_or_msg import PoissonMemberOrMessage
from typing import Dict, List
import json

class PoissonMessageOnWeb(Resource):

    def get(self) -> Response:

        #Checking authorization
        self.__uid: int = is_authorized() #<--- Grabbing the user id and checking if the user is authorized to access the endpoint

        #Grabbing the range of analysis
        self.__from: int | None = request.args.get("from", type = int)
        self.__until: int | None = request.args.get("until", type = int)

        #Checking the income values
        if self.__from is None or self.__until is None:
            abort(400, message = "Bad Request: you must deliver integers to 'from' and 'until' parameters")

        #Ignoring invalid values
        if self.__from < 0 or self.__from > self.__until:
            abort(422, message = "Forbidden values: 'from' must be positive and can't be lower than 'until'")

        #Grabbing Poisson probability if everything went fine
        self.__msg_volume: List[Dict[str, int]] = MessageDQL().get_msg_volume_per_day(server_id = self.__uid)
        self.__daily_vols: List[int] = [list(data.values())[0] for data in self.__msg_volume]#<--- Sorted daily volumes
        self.__msg_poisson: PoissonMemberOrMessage = PoissonMemberOrMessage()
        self.__prob: float = self.__msg_poisson.get_poisson_in_range(
            from_qtt = self.__from,
            until_qtt = self.__until,
            incrs = self.__daily_vols
        ) #<--- Getting the probability of having the aimed amount of messages tomorrow

        #Preparing and sending the response
        self.__resp: Response = make_response(
            json.dumps({
                "probability" : self.__prob,
                "from" : self.__from,
                "until" : self.__until
            }), 200
        )
        self.__resp.headers["Content-Type"] = "application/json" #<--- Informing that we are sending a JSON inside the string.
        refresh_jwt_or_cookie(self.__resp) #<--- Refresing the cookie or jwt (if it is about to expire)
        return self.__resp