import os
import sys
import dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
dotenv.load_dotenv(".env")
from time import sleep
from project.frameworks_and_drivers.databases.redis_db.rate_limit.token_bucket_per_user import TokenBucketPerUser

if __name__ == "__main__":
    sleep(20)
    TokenBucketPerUser.feed_buckets_in_parallel(interval = 1)