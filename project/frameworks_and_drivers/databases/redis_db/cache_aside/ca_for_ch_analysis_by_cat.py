from project.frameworks_and_drivers.databases.redis_db.cache_aside.cache_aside import CacheAside

class CacheAsideChannelAnalysisByCat(CacheAside):

    def __init__(self, server_id: int):
        self.key: str = f"ca_for_ch_analysis_by_cat_{server_id}"