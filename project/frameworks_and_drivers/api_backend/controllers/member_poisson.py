from flask_restful import Resource, abort
from flask import Response, request
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from typing import Tuple, Dict, List
from project.application.poisson_member_or_msg import PoissonMemberOrMessage
from project.frameworks_and_drivers.api_backend.middlewares.rate_blocker import rate_blocker

class MemberPoisson(Resource):

    def __init__(self):
        super().__init__()
        self.__DIST_SIZE: int = 20
        self.__MEMBER_DQL: MemberDQL = MemberDQL()

    def get(self) -> Response:
        
        rate_blocker() #<--- Rate blocker

        #Grabbing the URL data
        self.__server_id: int | None = request.args.get("server_id", type = int)
        self.__from_qtt: int | None = request.args.get("from_qtt", type = int)
        self.__until: int | None = request.args.get("until", type = int)
        self.__chart: int | None = request.args.get("chart", type = str)

        #Checking the income data
        input: Tuple[int, ...] = (self.__chart, self.__server_id, self.__from_qtt, self.__until)
        for data in input:
            if data is None:
                abort(400, message = "all query parameters must be filled")
        if self.__from_qtt < 0 or self.__until < self.__from_qtt:
            abort(400, message = "from_qtt must be positive and until can't be smaller than from_qtt")
        
        #Querying the database
        self.__dataset: Dict[str, Tuple[int, ...]] = self.__MEMBER_DQL.get_members_qtt(self.__server_id)
        self.__incrs: List[int | float] = [data[0] for data in self.__dataset.values()]

        #Checking the number of days
        if len(self.__incrs) < 7:
            abort(403, message = "You must have at least one weak of member data before doing this operation")
        
        pm: PoissonMemberOrMessage = PoissonMemberOrMessage()

        self.__prob: float = pm.get_poisson_in_range(
            from_qtt = self.__from_qtt,
            until_qtt = self.__until,
            incrs = self.__incrs)

        #If the requester doesn't want to see the image
        if self.__chart != "chart":
            
            self.__resp: Dict[str, str | float] = {
                "data" : self.__prob,
                "message" : "ok"
            }
        
            return self.__resp, 200

        self.__dist_discrete_points: List[Dict[int, float]] = pm.get_discrete_points(incrs = self.__incrs, until = self.__until, dist_size = self.__DIST_SIZE)
        self.__resp: Dict[str, str | List[Tuple[int, float]]] = {
            "message" : "ok",
            "data" : self.__dist_discrete_points,
            "probability": self.__prob
        }
        
        return self.__resp, 200