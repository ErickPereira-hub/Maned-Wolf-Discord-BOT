from .base_entity import BaseEntity

class MemberEntity(BaseEntity):

    def __init__(self,
                member_id: int,
                category: str | None,
                member_name: str | None,
                joined_at: str | None,
                account_create_at: str | None,
                server_id: int,
                deleted_at: str | None = None):
        self.member_id: int = member_id
        self.member_name: str | None = MemberEntity.empty_is_none(member_name)
        self.joined_at: str | None = MemberEntity.empty_is_none(joined_at)
        self.account_create_at: str | None = MemberEntity.empty_is_none(account_create_at)
        self.category: str | None = MemberEntity.empty_is_none(category)
        self.server_id: int = server_id
        self.deleted_at: str | None = deleted_at