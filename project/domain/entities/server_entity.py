import math
from .base_entity import BaseEntity

class ServerEntity(BaseEntity):

    def __init__(self,
                id: int,
                name: str | None,
                description: str | None,
                created_at: str | None,
                owner_name: str | None):
        self.id: int = id
        self.name: str | None = ServerEntity.empty_is_none(name)
        self.desc: str | None = ServerEntity.empty_is_none(description)
        self.created_at: str | None = ServerEntity.empty_is_none(created_at)
        self.owner_name: str | None = ServerEntity.empty_is_none(owner_name)