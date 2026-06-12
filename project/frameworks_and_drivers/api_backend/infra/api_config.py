from flask_restful import Api, Resource
from flask import Flask
from typing import Dict
from .http_request_body_args_singleton import HTTP_BODY_ARGS

class KernelApi:

    def __init__(self, routes: Dict[Resource, str]):
        self.__app: Flask = Flask(__name__)
        self.__api: Api = Api(self.__app)
        self.HTTP_INPUT = HTTP_BODY_ARGS
        self.__load_routes(routes)

    def __load_routes(self, routes: Dict[Resource, str]) -> None:
        for class_name, route in routes.items():
            #Registering a route of the api in the backend. It will embrace all HTTP methods related to such route.
            self.__api.add_resource(class_name, route)

    @property
    def api(self) -> Api:
        return self.__api

    @property
    def app(self) -> Flask:
        return self.__app