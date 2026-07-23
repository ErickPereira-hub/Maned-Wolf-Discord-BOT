from flask import Response, make_response
from flask_restful import Resource
from project.frameworks_and_drivers.api_backend.middlewares.refresh_cookie import refresh_jwt_or_cookie
from project.frameworks_and_drivers.databases.mysql_db.dql.messages_dql import MessageDQL
from typing import Dict, List
from project.frameworks_and_drivers.api_backend.controllers.extensions.poisson_web_extension import get_poisson_web_beginning
from project.application.poisson_member_or_msg import PoissonMemberOrMessage
import json

class PoissonMessageOnWeb(Resource):

    def get(self) -> Response:

        #Checking authorization and grabbing the data that came from the frontend
        self.__data: Dict[str, int] = get_poisson_web_beginning()
        self.__uid = self.__data["uid"]
        self.__from = self.__data["from"]
        self.__until = self.__data["until"]

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