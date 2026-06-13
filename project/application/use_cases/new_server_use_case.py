from typing import Dict, Any
from project.domain.entities import MemberEntity, ServerEntity, ChannelEntity

class NewServerUseCase:

    def __init__(self, JSON: Dict[str, Any]):
        """
        The JSON that gets into this constructor must follow the following structure:

        {
        "server_id": guild.id,
        "server_name": str(guild.name),
        "description": str(guild.description),
        "server_creation_date": str(guild.created_at),
        "owner_name": server_owner.global_name if server_owner is not None else "None",
        "members_id": [int(m["member_id"]) for m in members],
        "members_name": [str(m["member_name"]) for m in members],
        "mcategories": [str(m["category"]) for m in members],
        "they_joined_at": [str(m["joined_at"]) for m in members],
        "their_account_were_create_at": [str(m["account_create_at"]) for m in members],
        "channels_id": [int(c["channel_id"]) for c in channels],
        "channels_name": [str(c["channel_name"]) for c in channels],
        "types": [str(["type"]) for c in channels],
        "ccategories": [str(c["category"]) for c in channels],
        "are_nsfw": [str(c["is_nsfw"]) for c in channels]
        }

        Otherwise, an error will occur and the data won't be processed in the backend of the API.
        """
        self.__JSON: Dict[str, Any] = JSON
        self.__new_JSON: None | Dict[str, Any] = None #The method will set a better value for this attribute

    @property
    def aggregate_JSON(self) -> Dict[str, Any]:
        self.__new_JSON = {
            "server": ServerEntity(
                id = self.__JSON["server_id"],
                name = self.__JSON["server_name"],
                description = self.__JSON["description"],
                owner_name = self.__JSON["owner_name"],
                created_at = self.__JSON["server_creation_date"],
                member_qtt = len(self.__JSON["members_id"]) #<--- Evaluates the number of members inside the server
            ),
            "members_list": [
                MemberEntity(
                    member_id = self.__JSON["members_id"][_],
                    category = self.__JSON["mcategories"][_],
                    member_name = self.__JSON["members_name"][_],
                    joined_at = self.__JSON["they_joined_at"][_],
                    account_create_at = self.__JSON["their_account_were_create_at"][_],
                    server_id = self.__JSON["server_id"], # <--- From the server
                ) for _ in range(len(self.__JSON["members_id"]))], #<--- Detail: all members data are from the treated server and they are in the same order
            "channels_list": [
               ChannelEntity(
                   channel_id = self.__JSON["channels_id"][_],
                   channel_name = self.__JSON["channels_name"][_],
                   category = self.__JSON["ccategories"][_],
                   is_nsfw = self.__JSON["are_nsfw"][_],
                   server_id = self.__JSON["server_id"], # <--- From the server
               ) for _ in range(len(self.__JSON["channels_id"]))
            ]
        }
        return self.__new_JSON