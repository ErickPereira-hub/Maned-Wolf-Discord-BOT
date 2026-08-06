from project.frameworks_and_drivers.databases.redis_db.infra.redis_cnx_singleton import rcnx
import os

class loginBlocker:

    STARTING_VALUE: int = int(os.getenv("LOGIN_CHANCES"))
    TTL: int = int(os.getenv("TTL_FOR_LOGIN_RATELIMIT"))

    @classmethod
    def __gen_user_key(cls, sid: int) -> str:
        return f"login-{sid}"

    @classmethod
    def __create_user(cls, sid: int) -> None:
        key: str = cls.__gen_user_key(sid)
        rcnx.set(key, cls.STARTING_VALUE)
        rcnx.expire(key, cls.TTL)

    @classmethod
    def generate_or_takeout_chance(cls, sid: int) -> None:
        key: str = cls.__gen_user_key(sid)
        print(key, flush = True)
        #Checking existence
        if not bool(rcnx.exists(key)):
            cls.__create_user(sid) #<--- Creating the non-existed user
            return

        #if the user already exists, we will take out a chance
        ttl: int = rcnx.ttl(key)
        print(ttl, flush = True)
        rcnx.set(key, int(rcnx.get(key)) - 1)
        rcnx.expire(key, ttl) #<--- Redefining the expiration as the previous TTL in order to avoid reseting the TTL of the user

    @classmethod
    def check_if_user_has_chances(cls, sid: int) -> bool:
        #Return false if the user doesn't exist
        key: str = cls.__gen_user_key(sid)
        if not bool(rcnx.exists(key)):
            return False

        #Checking the quantity
        qtt: int = int(rcnx.get(key))
        print(qtt, flush = True)
        if qtt <= 0:
            return False
        return True

    @classmethod
    def delete_user(cls, sid: int) -> None:
        key: str = cls.__gen_user_key(sid)
        rcnx.delete(key) #<--- Deleting the user from redis