from flask_restful import Resource, abort
from flask import Response, request
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from typing import Tuple, Dict, List, Any
from project.frameworks_and_drivers.api_backend.middlewares.acumulative_freq_middleware import add_acum_freq_middleware
from project.application.use_cases.predict_poly_reg_use_case import predict_poly_reg_use_case
from project.frameworks_and_drivers.api_backend.middlewares.rate_blocker import rate_blocker
from project.frameworks_and_drivers.databases.redis_db.cache_aside.ca_for_member_predict import CacheAsideMemberPredict

class MemberPredict(Resource):

    def get(self) -> Response:

        rate_blocker() #<--- Rate blocker

        #Grabbing the inputs
        self.__sid: int = request.args.get("server_id", type = int)
        self.__day: int = request.args.get("day", type = int)

        #Unabling bad requests
        if self.__day > 3 or self.__day < 1 or self.__day is None:
            abort(400, message = "The maximum for 'day' is 3 and it must be an integer")
        if self.__sid is None:
            abort(400, message = "server id must be present")
        
        #Attribute that will be our initial dataset
        self.__dataset: Dict[str, Tuple[int, int, int]] | None = None

        #Querying the databases with cache-aside
        self.__cache_obj: CacheAsideMemberPredict = CacheAsideMemberPredict(server_id = self.__sid)
        if self.__cache_obj.exists_in_cache():
            self.__dataset = self.__cache_obj.fetch_cache()
        else:
            self.__dataset = MemberDQL().get_members_qtt(server_id = self.__sid)
            self.__cache_obj.insert_into_cache(JSON = self.__dataset)
        
        self.__dataset_completed: Dict[str, float | Dict[str, Tuple[int, int, int, int]]] = add_acum_freq_middleware(self.__dataset)

        #Checking the number of days
        if len(self.__dataset) < 10:
            abort(403, message = "Number of days is too slow!") #<--- Forbidden Access if the number of days is small because we need a large dataset as the base of the prediction.
        
        #Filtering the data
        self.__qtt_arr: List[int] = [data[3] for data in self.__dataset_completed["data"].values()]
        self.__qtt_pos: List[int] = [pos + 1 for pos in range(len(self.__qtt_arr))]
        self.__points: List[Tuple[int, int]] = list(zip(self.__qtt_pos, self.__qtt_arr))

            #Doing the prediction
        self.__resp_prediction: Dict[str, float | int] = predict_poly_reg_use_case(
            input = max(self.__qtt_pos) + self.__day,
            dataset = self.__points
            )

        #Organizing the data
        self.__ERR: float | int = self.__resp_prediction["error"]
        self.__poly: str = str(self.__resp_prediction["polynomial"])
        self.__tot_predicted_qtt: int | float = self.__resp_prediction["predicted_output"]

        #Sending the final response
        self.__response_json: Dict[str, Any] = {
            "error": self.__ERR,
            "poly": self.__poly,
            "result": self.__tot_predicted_qtt
        }
        return self.__response_json, 200