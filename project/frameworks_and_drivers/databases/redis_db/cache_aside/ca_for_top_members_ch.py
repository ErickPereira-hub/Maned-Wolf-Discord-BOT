from project.frameworks_and_drivers.databases.redis_db.cache_aside.cache_aside import CacheAside

class CacheAsideTopMembersByCh(CacheAside):

    def __init__(self, channel_id: int):
        self.key: str = f"ca_top_members_by_ch{channel_id}"