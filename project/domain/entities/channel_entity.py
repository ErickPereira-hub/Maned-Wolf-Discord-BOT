from .base_entity import BaseEntity

class ChannelEntity(BaseEntity):

    def __init__(self,
                channel_id: int,
                channel_name: str | None,
                category: str | None,
                is_nsfw: str | None,
                server_id: int):
        self.channel_id: int = channel_id
        self.channel_name: str | None = ChannelEntity.empty_is_none(channel_name)
        self.category: str | None = ChannelEntity.empty_is_none(category)
        self.is_nsfw: str | None = ChannelEntity.empty_is_none(is_nsfw)
        self.server_id: int = server_id