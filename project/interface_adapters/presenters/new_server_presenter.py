from project.domain.interfaces.presenter import Presenter
from typing import Dict, Any, List
from project.domain.entities.base_entity import BaseEntity

class NewServerPresenter(Presenter):

    def __init__(self, data: Dict[str, Any]):
        self.__ns_data: Dict[str, Any] = data
        self.__clean_data: Dict[str, Any] = None

    def get_data(self) -> Dict[str, Any]:
        self.__server: BaseEntity = self.__ns_data["server"]
        self.__ml: List[BaseEntity] = self.__ns_data["members_list"]
        self.__cl: List[BaseEntity] = self.__ns_data["channels_list"]
        self.__clean_data = {
            "server_data": {
                "id": self.__server.id,
                "name": self.__server.name,
                "description": self.__server.desc,
                "owner_name": self.__server.owner_name,
                "creation_date": self.__server.created_at
            },
            "members_data": [
                {
                    "id": m.member_id,
                    "name": m.member_name,
                    "category": m.category,
                    "joined_at": m.joined_at,
                    "account_create_at": m.account_create_at
                } for m in self.__ml
            ],
            "channels_data": [
               {
                   "id": c.channel_id,
                   "name": c.channel_name,
                   "category": c.category,
                   "created_at": c.created_at,
                   "is_nsfw": c.is_nsfw
               } for c in self.__cl
            ]
        }
        return self.__clean_data