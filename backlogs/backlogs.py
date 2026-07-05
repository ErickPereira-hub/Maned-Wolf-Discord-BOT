import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from time import sleep
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

if __name__ == "__main__":
    sleep(20)
    CacheBacklog.process_backlogs()