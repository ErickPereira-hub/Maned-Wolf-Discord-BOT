from concurrent.futures import ThreadPoolExecutor
import os
from typing import Dict, List, Callable
from requests import Response, get
import project.frameworks_and_drivers #<--- Important: this import starts the environmental variables that we need

def fetch_api(endpoint: Dict[str, str], status_list: List[int]) -> int:
    url: str = list(endpoint.keys())[0]
    http_method: str = list(endpoint.values())[0]
    resp: Response = http_method(url)
    status_list.append(resp.status_code)

def test_token_bucket_distributed() -> None:
    mocked_user_id: int = 1514414243003236523 #<--- Must be a real member id integrated with the bot.

    #Endpoints
    BASE_URL: str = os.getenv("BASE_URL")
    cred_extra: str = f"?member_id={mocked_user_id}"
    endpoints: List[Dict[str, Callable]] = [
        {BASE_URL + f"/member/poisson" + cred_extra : get},
        {BASE_URL + f"/member/analysis" + cred_extra : get},
        {BASE_URL + f"/member/predict" + cred_extra: get},
        {BASE_URL + f"/channel/top_active" + cred_extra : get},
        {BASE_URL + f"/channel/analysis" + cred_extra : get}
    ]

    #Getting more that the total capacity
    cpt: int = int(os.getenv("TOKEN_BUCKET_CAPACITY")) #<---- Capacity of the bucket per member
    over_capacity: int = cpt * 2 #<--- Number bigger than the capacity
    num_ops: int = max(over_capacity, len(endpoints)) #<--- number of allocated threads and requests
    status_list: List[int] = list() #<--- List of status code
    endpoint_selector: int = 0 #<--- Defines the chosen endpoint
    
    #Doing requests throughout threads
    with ThreadPoolExecutor(num_ops) as thread:
        for _ in range(num_ops): #<--- We will exceed the rate of rate limiting and force a 429 and we will go through all endpoints
            thread.submit(fetch_api, endpoint = endpoints[endpoint_selector], status_list = status_list)
            endpoint_selector += 1
            if endpoint_selector >= len(endpoints):
                endpoint_selector = 0 #Resenting the endpoint carroussel
    assert 429 in status_list #Failing the test if rate limiter wasn't achieved