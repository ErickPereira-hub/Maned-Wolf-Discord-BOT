from flask_restful import Resource, abort
from flask import Response, request
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from typing import Tuple, Dict, List, Any
from project.frameworks_and_drivers.api_backend.middlewares.acumulative_freq_middleware import add_acum_freq_middleware
from project.application.use_cases.predict_poly_reg_use_case import predict_poly_reg_use_case
from pprint import pprint
from project.application.use_cases.poisson_member_use_case import PoissonMemberUseCase

class MemberPoisson(Resource):

    def __init__(self):
        super().__init__()
        self.__DIST_SIZE: int = 20
        self.__MEMBER_DQL: MemberDQL = MemberDQL()

    def get(self) -> Response:

        #Grabbing the URL data
        self.__server_id: int | None = request.args.get("server_id", type = int)
        self.__from_qtt: int | None = request.args.get("from_qtt", type = int)
        self.__until: int | None = request.args.get("until", type = int)
        self.__show: int | None = request.args.get("show", type = str)

        #Checking the income data
        input: Tuple[int, ...] = (self.__show, self.__server_id, self.__from_qtt, self.__until)
        for data in input:
            if data is None:
                abort(400, message = "all query parameters must be filled")
        if self.__from_qtt < 1 or self.__until < self.__from_qtt:
            abort(400, message = "from_qtt must be positive and until can't be smaller than from_qtt")
        
        #Querying the database
        self.__dataset: Dict[str, Tuple[int, ...]] = self.__MEMBER_DQL.get_members_qtt(self.__server_id)
        self.__incrs: List[int | float] = [data[0] for data in self.__dataset.values()]

        #Checking the number of days
        if len(self.__incrs) < 7:
            abort(403, message = "You must have at least one weak of member data before doing this operation")
        
        pm_use_case: PoissonMemberUseCase = PoissonMemberUseCase()

        #If the requester doesn't want to see the image
        if self.__show != "show":
            
            self.__prob: float = pm_use_case.get_poisson_in_range(
                from_qtt = self.__from_qtt,
                until_qtt = self.__until,
                incrs = self.__incrs)
            
            self.__resp: Dict[str, str | float] = {
                "data" : self.__prob,
                "message" : "ok"
            }
        
            return self.__resp, 200
        
        #If the requester wants to see the data
        self.__region: range = range(1, self.__DIST_SIZE + 1)

        self.__dist_discrete_points: List[Tuple[int, float]] = list(zip(
            [pos for pos in self.__region],
            [
                pm_use_case.get_poisson_single_prob(input_qtt = pos, incrs = self.__incrs) for pos in self.__region
            ]))
        self.__resp: Dict[str, str | List[Tuple[int, float]]] = {
            "message" : "ok",
            "data" : self.__dist_discrete_points
        }
        
        return self.__resp, 200