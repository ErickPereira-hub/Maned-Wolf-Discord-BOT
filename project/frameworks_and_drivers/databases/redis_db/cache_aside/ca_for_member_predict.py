from project.frameworks_and_drivers.databases.redis_db.cache_aside.cache_aside import CacheAside

class CacheAsideMemberPredict(CacheAside):

    def __init__(self, server_id: int):
        self.key: str = f"ca_member_predict_{server_id}"