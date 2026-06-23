from project.frameworks_and_drivers.databases.redis_db.rate_limit.token_bucket_per_user import TokenBucketPerUser

if __name__ == "__main__":
    TokenBucketPerUser.feed_buckets_in_parallel(interval = 1)