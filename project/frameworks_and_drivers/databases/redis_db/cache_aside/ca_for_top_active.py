from project.frameworks_and_drivers.databases.redis_db.cache_aside.cache_aside import CacheAside

class CacheAsideTopActive(CacheAside):

    def __init__(self, server_id: int):
        self.key: str = f"ca_top_active_{server_id}"