from flask import Response, make_response
from flask_restful import Resource
from project.frameworks_and_drivers.api_backend.middlewares.refresh_cookie import refresh_jwt_or_cookie
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from project.frameworks_and_drivers.api_backend.controllers.extensions.poisson_web_extension import get_poisson_web_beginning
from project.application.poisson_member_or_msg import PoissonMemberOrMessage
from typing import Dict, List, Tuple
import json

class PoissonMemberOnWeb(Resource):

    def get(self) -> Response:

        #Checking authorization and grabbing the data that came from the frontend
        self.__data: Dict[str, int] = get_poisson_web_beginning()
        self.__uid = self.__data["uid"]
        self.__from = self.__data["from"]
        self.__until = self.__data["until"]

        #Grabbing Poisson probability if everything went fine
        self.__dataset: Dict[str, Tuple[int, ...]] = MemberDQL().get_members_qtt(self.__uid)
        self.__incrs: List[int | float] = [data[0] for data in self.__dataset.values()]
        pm: PoissonMemberOrMessage = PoissonMemberOrMessage()
        self.__prob: float = pm.get_poisson_in_range(
                    from_qtt = self.__from,
                    until_qtt = self.__until,
                    incrs = self.__incrs)
        
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