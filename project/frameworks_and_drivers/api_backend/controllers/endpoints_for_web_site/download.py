from flask import Response, request
from flask_restful import Resource, abort
from project.frameworks_and_drivers.api_backend.middlewares.refresh_cookie import refresh_jwt_or_cookie
from project.frameworks_and_drivers.api_backend.middlewares.auth_middleware import is_authorized
from project.frameworks_and_drivers.databases.mysql_db.dql.messages_dql import MessageDQL
import io
import csv
from typing import Dict, List

class DownloadMessageAuditLogs(Resource):

    def get(self) -> Response:
        self.__uid: int = is_authorized() #<--- Grabbing the user id and checking if the user is authorized to access the endpoint
        
        self.__audit_type: str | None = request.args.get("audit_type", type = str)

        #Checking the type of the audit
        if self.__audit_type is None or self.__audit_type not in ("update", "delete"):
            abort(400, message = "You must inform the audit_type with 'update' or 'delete'")

        self.__msg_obj: MessageDQL = MessageDQL()#<--- Object used to access the database methods

        self.__output: io.StringIO = io.StringIO()#<--- Object used to access the output csv at the end

        #If the admin wants to see the deleted messages
        if self.__audit_type == "delete":
            self.__data: List[Dict[str, int | str]] = self.__msg_obj.get_last_audit_deleted_messages(server_id = self.__uid)
            self.__writer: csv.DictWriter = csv.DictWriter(self.__output, fieldnames = ["message_id", "created_at", "deleted_at", "content"])
            self.__writer.writeheader()
            self.__writer.writerows(self.__data)
            self.__csv_file: str = self.__output.getvalue()
            self.__resp: Response = Response(
                self.__csv_file,
                status = 200,
                mimetype = "text/csv",
                headers = {"Content-Disposition" : "attachment; filename=deleted_messages.csv"}
            )
            refresh_jwt_or_cookie(self.__resp)
            return self.__resp
        
        if self.__audit_type == "update":
            self.__data: List[Dict[str, int | str]] = self.__msg_obj.get_last_audit_updated_messages(server_id = self.__uid)
            self.__writer: csv.DictWriter = csv.DictWriter(self.__output, fieldnames = ["message_id", "created_at", "updated_at", "old_content", "new_content"])
            self.__writer.writeheader()
            self.__writer.writerows(self.__data)
            self.__csv_file: str = self.__output.getvalue()
            self.__resp: Response = Response(
                self.__csv_file,
                status = 200,
                mimetype = "text/csv",
                headers = {"Content-Disposition" : "attachment; filename=updated_messages.csv"}
            )
            refresh_jwt_or_cookie(self.__resp)
            return self.__resp