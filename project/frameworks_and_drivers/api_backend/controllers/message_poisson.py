from flask_restful import Resource, abort
from flask import Response, request
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from typing import Tuple, Dict, List
from project.frameworks_and_drivers.databases.mysql_db.dql.messages_dql import MessageDQL
from project.frameworks_and_drivers.api_backend.middlewares.rate_blocker import rate_blocker
from project.application.poisson_member_or_msg import PoissonMemberOrMessage

class MessagePoisson(Resource):

    def __init__(self):
        super().__init__()
        self.__DIST_SIZE: int = 20
        self.__msg_volume: List[Dict[str, int]] | None = None

    def get(self) -> Response:
        
        rate_blocker()#<--- Blocking abuses

        #Grabbing the data
        self.__sid: int | None = request.args.get("server_id", type = int)
        self.__from: int | None = request.args.get("from", type = int)
        self.__until: int | None = request.args.get("until", type = int)
        self.__chart: str | None = request.args.get("chart", type = str)

        #Checking the income data
        self.__data: Tuple[int, int, int, str] = (self.__sid, self.__from, self.__until, self.__chart)
        for income_data in self.__data:
            if income_data is None:
                abort(400, message = "You must define \'chart\', \'server_id\', \'from\' and \'until\'")
        
        #Fetching the database
        self.__msg_volume = MessageDQL().get_msg_volume_per_day(server_id = self.__sid)
        
        #Checking if the server presents enough data for the operation
        if len(self.__msg_volume) < 7: #<--- Means that the server has less than 7 days of message registered by the bot.
            abort(403, message = "You don't have enough days of message data (minimum is 7 days)")
        
        self.__daily_vols: List[int] = [list(data.values())[0] for data in self.__msg_volume]#<--- Sorted daily volumes
        
        self.__msg_poisson: PoissonMemberOrMessage = PoissonMemberOrMessage()

        self.__prob: float = self.__msg_poisson.get_poisson_in_range(
            from_qtt = self.__from,
            until_qtt = self.__until,
            incrs = self.__daily_vols
        ) #<--- Getting the probability of having the aimed amount of messages tomorrow
        
        #If we aren't going to create a chart in the future
        if self.__chart != "chart":
            return {"data": self.__prob}, 200 #<--- differente from chart means that we just want to present the probability.

        self.__dist_discrete_points: List[Tuple[int, float]] = self.__msg_poisson.get_discrete_points(incrs = self.__daily_vols, until = self.__until, dist_size = self.__DIST_SIZE)
        self.__resp: Dict[str, float | List[Tuple[int, float]]] = {
            "data" : self.__dist_discrete_points,
            "probability": self.__prob
        }
        
        return self.__resp, 200