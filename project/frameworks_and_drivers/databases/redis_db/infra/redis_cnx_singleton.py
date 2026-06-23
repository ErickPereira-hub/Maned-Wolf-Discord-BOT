from redis import Redis

rcnx: Redis = Redis(
    host = "localhost",
    port = 6379,
    db = 0
)