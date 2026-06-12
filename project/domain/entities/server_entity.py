import math
from .base_entity import BaseEntity

class ServerEntity(BaseEntity):

    def __init__(self,
                id: int,
                name: str | None,
                description: str | None,
                created_at: str | None,
                member_qtt: int | None,
                owner_name: str | None):
        self.id: int = id
        self.name: str | None = ServerEntity.empty_is_none(name)
        self.desc: str | None = ServerEntity.empty_is_none(description)
        self.created_at: str | None = ServerEntity.empty_is_none(created_at)
        self.__member_qtt: int | None = member_qtt
        self.owner_name: str | None = ServerEntity.empty_is_none(owner_name)
    
    @property
    def member_qtt(self) -> None | int:
        if self.__member_qtt < 0 or math.floor(self.__member_qtt) != self.__member_qtt:
            return None #The value has no sense, so we return None
        return self.__member_qtt