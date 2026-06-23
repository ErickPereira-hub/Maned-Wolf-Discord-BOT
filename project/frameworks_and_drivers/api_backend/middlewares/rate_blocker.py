from flask_restful import abort
from flask import request
from project.frameworks_and_drivers.databases.redis_db.rate_limit.token_bucket_per_user import TokenBucketPerUser

def rate_blocker() -> None:

    #Grabbing the user id
    mid: int = request.args.get("member_id", type = int)
    if mid is None:
        abort(400, message = "\'member_id\' must be given")
    user_bucket: TokenBucketPerUser = TokenBucketPerUser(mid)
    allowed: bool = user_bucket.can_acces_api()
    if not allowed:
        abort(429, message = "Too many requests")