import jwt
import os
from datetime import datetime, timedelta
from typing import Any, Dict

class JwtFactory:

    def __init__(self,
                secret_key: str = os.getenv("JWT_SECRET_KEY"),
                algorithm: str = os.getenv("JWT_ALGORITHM"),
                ttl_jwt: str = os.getenv("JWT_TTL"),
                max_refresh_time_in_minutes: str = os.getenv("JWT_MAX_REFRESH_TIME_IN_MINUTES")):
        self.__skey: str = secret_key
        self.__agt: str = algorithm
        self.__ttl_jwt: int = int(ttl_jwt) #<--- TTL of the jwt token in seconds
        self.__max_refresh_time: int = int(max_refresh_time_in_minutes)
    
    def __generate_new_token(self, uid: int) -> str:
        print(self.__ttl_jwt)
        self.__token: str = jwt.encode(
            {
                "exp" : datetime.utcnow() + timedelta(seconds = self.__ttl_jwt),
                "uid" : uid
            },
            algorithm = self.__agt,
            key = self.__skey
            )
        return self.__token
    
    def get_new_jwt_token(self, uid: int) -> str:
        return self.__generate_new_token(uid)
    
    def get_refreshed_jwt_token(self, token) -> str | None:

        #Defining the payload
        self.__payload: None | Dict[str, Any] = None
        
        #Grabbing the payload of the token
        try:
            self.__payload = jwt.decode(token, key = self.__skey, algorithms = self.__agt)
        except jwt.ExpiredSignatureError: #<--- JWT has expired
            return None #<--- None is return just for the case of an expiration time in the TTL
        else:
            self.__ttl: datetime = datetime.utcfromtimestamp(self.__payload["exp"]) #<--- TTL in datetime
            self.__time_diff: timedelta = self.__ttl - datetime.utcnow() #<--- Difference of time between the expiring date and now in UTC
            if self.__time_diff < timedelta(minutes=self.__max_refresh_time): #<--- If the token is about to expire, we return a new token with refreshed TTL
                return self.__generate_new_token(self.__payload["uid"])
            else: #<--- If the token is not about to expire, we return the same token
                return token
            
    def extract_payload(self, jwt_token: str) -> Dict[str, Any] | None:
        self.__ext_payload: Dict[str, Any] | None = None
        try:
            self.__ext_payload = jwt.decode(jwt_token, key = self.__skey, algorithms = self.__agt)
        except jwt.ExpiredSignatureError:
            return None #<--- Means that the JWT has been expired
        else:
            return self.__ext_payload