from flask_restful import abort, Resource, reqparse
from typing import Any, Dict
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from pprint import pprint
from project.interface_adapters.presenters.new_server_presenter import NewServerPresenter
from project.application.use_cases.new_server_use_case import NewServerUseCase
from project.frameworks_and_drivers.databases.mysql_db.dml.transactions.new_server_in_transaction import NewServerInTransaction

class NewServerIn(Resource):
    
    def post(self):
        self.__args: Dict[str, Any] = HTTP_BODY_ARGS.args_new_server.parse_args()
        #Checking if everything is ok
        for key, value in self.__args.items():
            if key != "description" and value is None:
                abort(400, message = "An important information about the server wasn't given")
        
        self.__transformed_data: Dict[str, Any] = NewServerPresenter(NewServerUseCase(self.__args).aggregate_JSON).get_data()
        #Sending the dataset to the database
        NewServerInTransaction.send_new_server_data(nw_presenter = self.__transformed_data)

        #Must run if everything went well
        self.__GOOD_JSON_RESPONSE: Dict[str, str] = {"message": "Ok"}
        return self.__GOOD_JSON_RESPONSE, 201