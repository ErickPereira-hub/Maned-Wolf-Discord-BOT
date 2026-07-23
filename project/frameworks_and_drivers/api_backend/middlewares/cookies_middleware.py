from flask import Response
import os

def send_cookie(resp: Response, key: str, data: str) -> None:
    resp.set_cookie(
        key = key,
        value = data,
        max_age = int(os.getenv("COOKIE_TTL")),
        httponly = True, #<--- JS won't be able to read the token
        secure = True, #<--- Communication will be done in HTTPS
        samesite = "none"
    )