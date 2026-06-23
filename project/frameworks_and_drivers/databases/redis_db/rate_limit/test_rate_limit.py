#This script has the objective of testing the Rate limitng of the api
import os
from requests import get
import time

def test_api():
    URL: str = "http://127.0.0.1:5000" + f"/channel/analysis?server_id=1355219891275436133&style=category&member_id=1514414243003236523"
    resp = get(URL)
    print(f"status >> {resp.status_code}")

from concurrent.futures import ThreadPoolExecutor

if __name__ == "__main__":
    x = 12
    with ThreadPoolExecutor(max_workers = x) as task:
        t1 = time.time()
        for _ in range(x):
            task.submit(test_api)
        t2 = time.time()
    print(f"time to run >> {(1000 * (t2 - t1)):.0f} ms")