from project.domain.interfaces.rate_limit_world import RateLimitWorld
from project.frameworks_and_drivers.databases.redis_db.infra.redis_cnx_singleton import rcnx
import os
from typing import List, Dict
from time import sleep, time
from datetime import datetime

class TokenBucketPerUser(RateLimitWorld):
    
    FREQ: int = int(os.getenv("QTT_NEW_TOKENS_PER_SECOND"))
    CAP: int = int(os.getenv("TOKEN_BUCKET_CAPACITY"))
    TTL: int = 1200

    def __init__(self, user_id: int):
        self.__key: str = f"TB_{user_id}"

    def __create_bucket(self) -> None:
        rcnx.set(self.__key, TokenBucketPerUser.CAP) #<--- Creating the bucket with maximum capacity
        rcnx.expire(self.__key, TokenBucketPerUser.TTL) #<--- The bucket expires in 20 min
    
    def can_acces_api(self) -> bool:

        self.__resp: bool = False

        #Creating the bucket for the non-existence case
        has_bucket: bool =  bool(rcnx.exists(self.__key))
        if not has_bucket:
            self.__create_bucket()

        self.__tokens_qtt: int = int(rcnx.get(self.__key).decode()) #<--- Quantity of tokens of the user
        
        #checking if we have tokens inside the api to allow or block access
        if self.__tokens_qtt > 0:
            self.__resp = True
            rcnx.decr(self.__key, 1)  #<--- Loosing one token due to API usage
        
        return self.__resp
    
    @classmethod
    def feed_buckets_in_parallel(cls, interval: float | int = 1) -> None:
        
        while True:
            t_start: float = time() #<--- Starting time of the loop

            #Important variables for aggregation
            sum_of_ttls: float | int = 0
            sum_of_tokens: int = 0
            zero_tokens_qtt: int = 0

            #Getting all keys related to a token bucket
            keys: List[bytes] = rcnx.keys("TB_*")

            keys_str: List[str] = [key.decode() for key in keys]#<--- same list as before, but with strings instead of bytes
            
            size: int = len(keys_str)#<--- Number of buckets and number of active users of the API
            
            #Feeding our buckets
            for key in keys_str:
                
                #Getting the quantity of tokens of the bucket and the ttl
                token_qtt: int = int(rcnx.get(key).decode())
                ttl: int = rcnx.ttl(key) #<--- TTL of the bucket in seconds
                
                sum_of_ttls += ttl #Incrementing the TTL sum
                sum_of_tokens += token_qtt #Incrementing the token

                if token_qtt == 0:
                    zero_tokens_qtt += 1 #429 activated for one user

                #Feeding the bucket with new tokens when needed
                if token_qtt + cls.FREQ <= cls.CAP:
                    rcnx.incr(key, cls.FREQ)
                else:
                    rcnx.set(key, cls.CAP)
                    rcnx.expire(key, ttl) #Keeping the same expire time to the key

            t_end: float = time() #<--- End time
            t_int: float = t_end - t_start #<--- Interval of time taken to do CRUD in Redis

            BACKLOG_MSG: str = f"""
            {'='*50}
            [ {datetime.utcnow()} ]
            quantity of buckets (one for each user) >> \033[36m{size}\033[m

            Average data for the users >> 
                    ttl: \033[32m{sum_of_ttls / size} sec\033[m
                    tokens: \033[32m{sum_of_tokens / size}\033[m
            
            Too many requests >> \033[{"31" if zero_tokens_qtt != 0 else "32"}m{zero_tokens_qtt}\033[m

            Time to run: \033[{"31m" if t_int > 500 else "32m"}{(t_int * 1000):.0f}ms\033[m
            """ if size != 0 else "Theres no active user"
            print(BACKLOG_MSG)

            #Correcting the delay when there is too many users
            sleep(interval - t_int if t_int < interval else 0)