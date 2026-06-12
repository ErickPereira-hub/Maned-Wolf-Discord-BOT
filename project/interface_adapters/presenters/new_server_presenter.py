from project.domain.interfaces.presenter import Presenter
from typing import Dict, Any

class NewServerPresenter(Presenter):

    def __init__(self, data: Dict[str, Any]):
        self.__ns_data: Dict[str, Any] = data
        self.__clean_data: Dict[str, Any] = None

    def get_data(self) -> Dict[str, Any]:
        self.__server = self.__ns_data["server"]
        self.__ml = self.__ns_data["members_list"]
        self.__cl = self.__ns_data["channels_list"]
        self.__clean_data = {
            "server_data": {
                "id": self.__server.id,
                "name": self.__server.name,
                "description": self.__server.description,
                "owner_name": self.__server.owner_name,
                "member_qtt": self.__server.member_qtt,
                "creation_date": self.__server.creation_date
            },
            "members_data": [
                {
                    "id": self.__ml.member_id,
                    "name": self.__ml.member_name,
                    "category": self.__ml.category,
                    "joined_at": self.__ml.joined_at,
                    "account_create_at": self.__ml.account_create_at
                } for m in self.__ml
            ],
            "channels_data": [
               {
                   "id": self.__cl.channel_id,
                   "name": self.__cl.channel_name,
                   "type": self.__cl.type,
                   "category": self.__cl.category,
                   "is_nsfw": self.__cl.is_nsfw
               } for c in self.__cl
            ]
        }
        return self.__clean_data