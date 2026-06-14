from typing import Dict
from flask_restful import Resource
from project.frameworks_and_drivers.api_backend.controllers.new_server_in import NewServerIn
from project.frameworks_and_drivers.api_backend.controllers.msg import Msg
from project.frameworks_and_drivers.api_backend.controllers.member import Member
from project.frameworks_and_drivers.api_backend.controllers.channel import Channel

routes: Dict[Resource, str] = {
    NewServerIn : "/new-server",
    Msg : "/msg",
    Member : "/member",
    Channel: "/channel"
}