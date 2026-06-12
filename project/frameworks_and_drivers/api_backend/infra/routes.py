from typing import Dict
from flask_restful import Resource
from project.frameworks_and_drivers.api_backend.controllers.new_server_in import NewServerIn

routes: Dict[Resource, str] = {
    NewServerIn : "/new-server"
}