from redis import Redis

rcnx: Redis = Redis(
    host = "redis_db",
    port = 6379,
    db = 0
)