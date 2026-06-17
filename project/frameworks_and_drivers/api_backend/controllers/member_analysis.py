from flask_restful import abort, Resource
from typing import Dict, Tuple
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from flask import request
from project.frameworks_and_drivers.api_backend.middlewares.acumulative_freq_middleware import add_acum_freq_middleware
from project.application.utils.std_deviation import get_std_deviation
import math

class MemberAnaysis(Resource):

    def __init__(self):
        super().__init__()
        self.__MEMBER_DQL_SINGLETON: MemberDQL = MemberDQL()

    def get(self):
        self.__server_id: int | None = request.args.get("server_id", type = int)

        #Checking the server_id
        if self.__server_id is None:
            abort(400, message = "The server id wasn't given")

        #Grabbing the quantities of members for each day
        self.__data: Dict[str, Tuple[int, int, int]] = self.__MEMBER_DQL_SINGLETON.get_members_qtt(server_id = self.__server_id)
        self.__complete_data = add_acum_freq_middleware({"message": "ok", "data": self.__data})
        
        return self.__complete_data, 200