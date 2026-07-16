from flask_restful import abort, Resource
from typing import Any, Dict, Tuple
from project.frameworks_and_drivers.databases.mysql_db.dql.member_dql import MemberDQL
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_member import MemberDML
from project.frameworks_and_drivers.api_backend.infra.http_request_body_args_singleton import HTTP_BODY_ARGS
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_msg import MessageDML
from project.frameworks_and_drivers.databases.mysql_db.dql.channel_dql import ChannelDQL
from project.frameworks_and_drivers.databases.mysql_db.dml.dml_channel import ChannelDML
from flask import request, Response
from project.frameworks_and_drivers.api_backend.controllers.extensions.check_server_extension import dismish_non_servers

class Msg(Resource):
    
    def __init__(self):
        super().__init__()
        self.__MSG_DB_OBJ: MessageDML = MessageDML()
        self.__MEMBER_DB_OBJ_DQL: MemberDQL = MemberDQL()
        self.__MEMBER_DB_OBJ_DML: MemberDML = MemberDML()
        self.__CHANNEL_DB_OBJ_DQL: ChannelDQL = ChannelDQL()
        self.__CHANNEL_DB_OBJ_DML: ChannelDML = ChannelDML()

    def post(self) -> Response:
        self.__args: Dict[str, Any] = HTTP_BODY_ARGS.args_new_msg.parse_args()
        #Checking if everything is ok with the message
        self.__important: Tuple[str] = ("msg_id", "author_id", "channel_id", "server_id")
        for key in self.__important:
            if self.__args[key] is None:
                abort(400, message = "An important information about the server wasn't given")
        dismish_non_servers(self.__args["server_id"])
        #Checking if the user who sent the message exists in the database
        self.__signal_existence_of_member: bool = self.__MEMBER_DB_OBJ_DQL.check_existence(self.__args["server_id"], self.__args["author_id"])
        if not self.__signal_existence_of_member:
            self.__MEMBER_DB_OBJ_DML.send_to_db(
                member_id_disc = self.__args["author_id"],
                member_name = self.__args["mname"],
                category = self.__args["mcategory"],
                joined_at = self.__args["mjoined_at"],
                account_create_at = self.__args["maccount_create_at"],
                server_id = self.__args["server_id"]
            )

        #Checking if the channel where the message was sent exists in the database
        self.__signal_existence_of_channel: bool = self.__CHANNEL_DB_OBJ_DQL.check_existence(
            server_id = self.__args["server_id"],
            ch_id = self.__args["channel_id"]
        )
        if not self.__signal_existence_of_channel:
            self.__CHANNEL_DB_OBJ_DML.send_to_db(
                channel_id = self.__args["channel_id"],
                channel_name = self.__args["cname"],
                category = self.__args["ccategory"],
                is_nsfw = self.__args["cis_nsfw"],
                server_id = self.__args["server_id"]
            )

        #Sending the dataset to the database
        self.__MSG_DB_OBJ.send_to_db(
            msg_id = self.__args["msg_id"],
            msg_txt = self.__args["msg_text"],
            msg_date = self.__args["msg_date"],
            msg_edited_at = self.__args["msg_edited_at"],
            author_id = self.__args["author_id"],
            channel_id = self.__args["channel_id"]
        )

        #Must run if everything went well
        self.__GOOD_JSON_RESPONSE: Dict[str, str] = {"message": "Ok"}
        return self.__GOOD_JSON_RESPONSE, 201
    
    def delete(self) -> Response:
        self.__msg_id: int | None = request.args.get("msg_id", type = int)
        #Checking the id
        if self.__msg_id is None:
            return {"message": "You must deliver an id inside the 'msg_id' in the URL"}, 400
        #Deleting the data
        self.__MSG_DB_OBJ.del_in_db(self.__msg_id)
        return {"message": f"Message of id {self.__msg_id} has been successfully deleted"}, 200

    def patch(self) -> Response:
        self.__msg_id: int | None = request.args.get("msg_id", type = int)
        self.__msg_content: str | None = request.args.get("msg_new_txt", type = str)
        #Checking the id
        if self.__msg_id is None:
            return {"message": "You must deliver an id inside the 'msg_id' in the URL"}, 400
        #Updating the database
        self.__MSG_DB_OBJ.update_in_db(
            msg_id = self.__msg_id,
            new_txt = self.__msg_content
        )
        return {"message": f"Message of id {self.__msg_id} has been changed"}, 200