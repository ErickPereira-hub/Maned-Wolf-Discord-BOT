from project.frameworks_and_drivers.databases.redis_db.cache_aside.cache_aside import CacheAside

class CacheAsideTopMembersByServer(CacheAside):

    def __init__(self, server_id: int):
        self.key: str = f"ca_top_members_by_server{server_id}"