from flask_restful import abort, Resource, reqparse
from typing import Any, Dict
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from project.interface_adapters.presenters.new_server_presenter import NewServerPresenter
from project.application.use_cases.new_server_use_case import NewServerUseCase
from project.frameworks_and_drivers.databases.mysql_db.dml.transactions.new_server_in_transaction import NewServerInTransaction
from flask import Response, request
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_server import ServerDML
from project.application.utils.token_gen import TokenFactory
from werkzeug.security import generate_password_hash
from project.frameworks_and_drivers.api_backend.controllers.extensions.check_server_extension import dismish_non_servers

class Server(Resource):
    
    def post(self) -> Response:
        self.__args: Dict[str, Any] = HTTP_BODY_ARGS.args_new_server.parse_args()
        #Checking if everything is ok
        for key, value in self.__args.items():
            if key != "description" and value is None:
                abort(400, message = "An important information about the server wasn't given")

        self.__server_token: str = TokenFactory.gen_token() #<--- Token of 8 bytes

        self.__transformed_data: Dict[str, Any] = NewServerPresenter(NewServerUseCase(self.__args).aggregate_JSON).get_data()
        #Sending the dataset to the database
        NewServerInTransaction.send_new_server_data(nw_presenter = self.__transformed_data, secured_token = generate_password_hash(self.__server_token))

        #Must run if everything went well
        self.__GOOD_JSON_RESPONSE: Dict[str, str] = {"token": self.__server_token}
        return self.__GOOD_JSON_RESPONSE, 201
    
    def delete(self) -> Response:
        self.__sid: int = request.args.get("server_id", type = int)

        if self.__sid is None:
            abort(400, message = "The server_id must be given")

        #Deleting the data from the database
        ServerDML().del_in_db(self.__sid)

        return "", 200